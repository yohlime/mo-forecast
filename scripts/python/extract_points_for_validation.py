# Description: Extract fcst at station locations for validation
# Author: Kevin Henson
# Last edited: May 26, 2022

from pathlib import Path
import pandas as pd
import xarray as xr

from __const__ import tz, script_dir

site_df = pd.read_csv(script_dir / "python/resources/csv/stations_lufft.csv")

def extract_points_for_validation(ds_dict, out_dir):
    init_dt = pd.to_datetime(
        list(ds_dict.values())[0].time.values[0], utc=True
    ).astimezone(tz)

    new_ds_dict = {}
    for k, ds in ds_dict.items():
        _ds = []

        # region temp
        print("Processing temperature...")
        da = ds["temp"].mean("ens")
        da.name = "temp"
        _ds.append(da)
        da = ds["temp"].min("ens")
        da.name = "tempMin"
        _ds.append(da)
        da = ds["temp"].max("ens")
        da.name = "tempMax"
        _ds.append(da)
        # end region temp

        # region rain
        print("Processing chance of rain...")
        _da = ds["rain"]

        da = _da.mean("ens")
        da.name = "rain"
        _ds.append(da)
        # end region rain

        # region relative humidity
        print("Processing relative humidiy...")
        _da = ds["rh"]

        da = _da.mean("ens")
        da.name = "rh"
        _ds.append(da)
        # end region relative humidity

        # region heat index
        print("Processing heat index...")
        _da = ds["hi"]

        da = _da.mean("ens")
        da.name = "hi"
        _ds.append(da)
        # end region heat index

        new_ds_dict[k] = xr.merge(_ds)

    out_df = []
    for idx, r in site_df.iterrows():
        df_dict = {}
        for k, ds in new_ds_dict.items():
            _df = ds.sel(lon=r["lon"], lat=r["lat"], method="nearest").to_dataframe()
            _df.drop(columns=["lon", "lat"], inplace=True)
            _df.reset_index(inplace=True)
            _df.rename(columns={"time": "timestamp"}, inplace=True)
            _df["timestamp"] = (
                _df["timestamp"]
                .dt.tz_localize("UTC")
                .dt.tz_convert(tz)
                .dt.strftime("%Y-%m-%dT%H:00:00")
            )
            df_dict[k] = _df.to_dict(orient="records")
        _out_df = r.to_dict()
        _out_df["id"] = r["name"]
        _out_df["forecast"] = df_dict
        out_df.append(_out_df)

    out_df = pd.DataFrame(out_df)
    out_file = Path(out_dir) / f"forecast_lufft_stations_{init_dt.strftime('%Y-%m-%d_%H')}PHT.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_df.set_index("id").to_json(
        out_file, orient="index", indent=2, double_precision=2
    )
