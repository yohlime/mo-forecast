import sys
import getopt
from pathlib import Path
from datetime import timedelta
import pandas as pd
import xarray as xr
import pytz

from wrf import omp_set_num_threads, omp_get_max_threads

from __const__ import wrf_dirs, wrf_forecast_days, script_dir
from __helper__ import wrf_getvar


omp_set_num_threads(omp_get_max_threads())
print(f"Using {omp_get_max_threads()} threads...")

RAIN_CHANCE_ENUM = ["NoChance", "Low", "Medium", "High"]

site_df = pd.read_csv(script_dir / "python/input/csv/cities.csv")
tz = pytz.timezone("Asia/Manila")


def main(wrf_outs, out_dir):
    init_dt = pd.to_datetime(
        wrf_getvar(wrf_outs[0], "T2", 0).time.values, utc=True
    ).astimezone(tz)

    timeidxs = [day * 24 for day in range(1, wrf_forecast_days + 1)]

    ds = []

    # region wpd
    print("Processing wpd...")
    _da = []
    for t in timeidxs:
        t0 = t - 24
        __da = [wrf_getvar(wrf_outs, "wpd", _t) for _t in range(t0, t)]
        ts = pd.to_datetime(__da[-1].time.values) + timedelta(hours=1)
        __da = xr.concat(__da, "time").sum("time")
        __da = __da.assign_coords(time=ts)
        _da.append(__da)
    _da = xr.concat(_da, "time")
    _da = _da.drop(["level", "wspd_wdir"])

    __da = _da.mean("key_0")
    __da.name = "wndPow"
    ds.append(__da)
    __da = _da.max("key_0")
    __da.name = "wndPowMax"
    ds.append(__da)
    # end region wpd

    # region ppv
    print("Processing ppv...")
    _da = []
    for t in timeidxs:
        t0 = t - 24
        __da = [wrf_getvar(wrf_outs, "ppv", _t) for _t in range(t0, t)]
        ts = pd.to_datetime(__da[-1].time.values) + timedelta(hours=1)
        __da = xr.concat(__da, "time").sum("time")
        __da = __da.assign_coords(time=ts)
        _da.append(__da)
    _da = xr.concat(_da, "time")

    __da = _da.mean("key_0")
    __da.name = "solPow"
    ds.append(__da)
    __da = _da.max("key_0")
    __da.name = "solPowMax"
    ds.append(__da)
    # end region ppv

    # region temp
    print("Processing temperature...")
    _da = [wrf_getvar(wrf_outs, "T2", t) for t in timeidxs]
    _da = xr.concat(_da, "time")
    _da = _da - 273.15

    __da = _da.min("key_0")
    __da.name = "tempMin"
    ds.append(__da)
    __da = _da.max("key_0")
    __da.name = "tempMax"
    ds.append(__da)
    # end region temp

    # region wind
    print("Processing wind...")
    u = [wrf_getvar(wrf_outs, "ua", t, levels=850, interp="pressure") for t in timeidxs]
    u = xr.concat(u, "time")
    v = [wrf_getvar(wrf_outs, "va", t, levels=850, interp="pressure") for t in timeidxs]
    v = xr.concat(v, "time")
    _da = u.copy()
    _da.values = (u.values ** 2 + v.values ** 2) ** 0.5
    _da.values = _da.values * 3.6  # convert to kph
    _da = _da.drop("level")

    __da = _da.min("key_0")
    __da.name = "wspdMin"
    ds.append(__da)
    __da = _da.max("key_0")
    __da.name = "wspdMax"
    ds.append(__da)
    # end region wind

    # region rainchance
    print("Processing chance of rain...")
    _da = [wrf_getvar(wrf_outs, "prcp", t) for t in timeidxs]
    for i, __da in enumerate(_da[1:]):
        _da[i + 1].values = __da.values - _da[i].values
    _da = xr.concat(_da, "time")
    _da = _da.where(_da <= 0.2, 1)
    _da = _da.where(_da > 0.2, 0)
    __da = _da.sum("key_0")
    __da.name = "rainChance"
    ds.append(__da)
    # end region rainchance

    ds = xr.merge(ds)
    ds = ds.assign_coords(
        west_east=ds.lon[0, :].values, south_north=ds.lat[:, 0].values
    )
    ds = ds.drop(["lon", "lat", "xtime"])
    ds = ds.rename({"west_east": "lon", "south_north": "lat"})

    out_df = []
    for idx, r in site_df.iterrows():
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
        _df["rainChance"] = _df["rainChance"].apply(lambda r: RAIN_CHANCE_ENUM[int(r)])
        _out_df = r.to_dict()
        _out_df["id"] = r["name"]
        _out_df["forecast"] = _df.round(1).to_dict(orient="records")
        out_df.append(_out_df)

    out_df = pd.DataFrame(out_df)
    out_file = Path(out_dir) / f"forecast_{init_dt.strftime('%Y-%m-%d_%H')}PHT.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_df.set_index("id").to_json(out_file, orient="index", indent=2)


if __name__ == "__main__":
    wrf_out = ""
    out_dir = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile=", "odir="])
    except getopt.GetoptError:
        print("test.py -i <wrf_out file> -o <output dir>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("test.py -i <wrf_out file> -o <output dir>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            wrf_out = arg
        elif opt in ("-o", "--odir"):
            out_dir = Path(arg)
            out_dir.mkdir(parents=True, exist_ok=True)
    wrf_outs = [d / wrf_out for d in wrf_dirs]
    main(wrf_outs, out_dir)
