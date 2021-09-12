#!/usr/bin/env python
# coding: utf-8

yyyymmdd = '2021-09-11'
init = '08'
OUT_DIR = '/home/modelman/forecast/output/summary/json/20210911/00'
IN_DIR = '/home/modelman/forecast/output/timeseries/csv_cities/20210911/00'
ST_DIR = '/home/modelman/forecast/scripts/timeseries/csv'
CH_DIR = '/home/modelman/forecast/scripts/rainchance/csv'

from pathlib import Path
import pandas as pd
import numpy as np


RAIN_CHANCE_ENUM = ["NoChance", "Low", "Medium", "High"]

stn_df = pd.read_csv(Path(ST_DIR) / "cities.csv")

out_df = []
for i, stn_info in stn_df.iterrows():
    stn_name = stn_info["name"].replace(" ", "")
    df = pd.read_csv(
        Path(IN_DIR) / f"{stn_name}_forecast_{yyyymmdd}_{init}PHT.csv",
        na_values="-999000000",
    )
    df.columns = df.columns.str.lower()

    df.rename(columns={"t": "temp"}, inplace=True)

    # Temperature: convert to celsius
    df["temp"] = df["temp"] - 273.15

    # Wind power potential: convert from WINDPOW to [MW]
    a = 0.5  # constant
    p = 1.23  # air density
    r = 52  # blade length of turbine (radius)
    cp = 0.4  # power coefficient
    turb = 4  # assume 4 wind turbines in one hectare
    sw_area = 8495  # swept area of turbine

    # Wind power potential equation [MW]
    df["wpd"] = turb * (a * p * sw_area * cp * df["windpow"]) / 1000000

    # Solar power potential: convert from GHI
    c1 = -3.75
    c2 = df["temp"] * 1.14
    c3 = df["ghi"] * 0.0175
    t_cell = c1 + c2 + c3
    t_ref = 25
    n_cell = 0.12 * (
        (df["ghi"] * 0 + 1) - 0.0045 * (t_cell - t_ref) + 0.1 * np.log10(df["ghi"])
    )
    s_panel = 7200  # estimated solar panel number in 1 hectare
    df["pvout"] = (df["ghi"] * n_cell * s_panel) / 1000000

    # GHI: convert to [kW/m^2]
    df["ghi"] = df["ghi"] / 1000

    # Prepare and extract summary table
    day_df = []
    start = 0
    end = 121
    for day in range(1, 6):
        dc = pd.read_csv(
            Path(CH_DIR) / f"{yyyymmdd}_{init}PHT_{stn_name}_chance.csv",
            names=["rainChance"],
        )
        next_t = (24 * day) + 1
        spow = df["pvout"][start:next_t]
        wpow = df["wpd"][start:next_t]
        temp = df["temp"][start:next_t]
        wspd = df["ws10"][start:next_t]
        wspd = wspd * 3.6  # convert to kph
        rain = df["pr"][start:next_t]
        rain_chance_idx = dc["rainChance"][day - 1]

        day_df.append(
            dict(
                day=day,
                timestamp=f"{yyyymmdd}T{init}:00:00",
                solPow=spow.mean(),
                solPowMin=spow.min(),
                solPowMax=spow.max(),
                wndPow=wpow.mean(),
                wndPowMin=wpow.min(),
                wndPowMax=wpow.max(),
                temp=temp.mean(),
                tempMin=temp.min(),
                tempMax=temp.max(),
                wspd=wspd.mean(),
                wspdMin=wspd.min(),
                wspdMax=wspd.max(),
                rain=rain.sum(),
                rainChance=RAIN_CHANCE_ENUM[rain_chance_idx],
            )
        )

    _out_df = stn_info.to_dict()
    _out_df["id"] = stn_name
    _out_df["forecast"] = pd.DataFrame(day_df).round(1).to_dict(orient="records")
    out_df.append(_out_df)

out_df = pd.DataFrame(out_df)
out_file = Path(OUT_DIR) / f"forecast_{yyyymmdd}_{init}PHT.json"
out_file.parent.mkdir(parents=True, exist_ok=True)
out_df.set_index("id").to_json(out_file, orient="index", indent=2)

out_file = Path(OUT_DIR) / "../../forecast_latest.json"
out_df.set_index("id").to_json(out_file, orient="index", indent=2)
