import os
import sys
import getopt
from pathlib import Path
from datetime import timedelta
import pandas as pd
import xarray as xr
import pytz

from wrf import omp_set_num_threads, omp_get_max_threads

from __const__ import wrf_dirs, wrf_forecast_days
from __helper__ import wrf_getvar
from plot_maps import plot_maps
from plot_web_maps import plot_web_maps
from extract_points import extract_points


omp_set_num_threads(int(os.getenv("SLURM_NTASKS", 4)))
print(f"Using {omp_get_max_threads()} threads...")

tz = pytz.timezone("Asia/Manila")


def main(wrf_outs, out_dir):
    timeidxs = [day * 24 for day in range(1, wrf_forecast_days + 1)]

    ds = []

    # region rain
    print("Processing rain...")
    _da = [wrf_getvar(wrf_outs, "prcp", t) for t in timeidxs]
    for i, __da in enumerate(_da[1:]):
        _da[i + 1].values = __da.values - _da[i].values
    _da = xr.concat(_da, "time")
    _da.name = "rain"
    ds.append(_da)
    # endregion rain

    # region temp
    print("Processing 2m temperature...")
    _da = [wrf_getvar(wrf_outs, "T2", t) for t in timeidxs]
    _da = xr.concat(_da, "time")
    _da = _da - 273.15
    _da.name = "temp"
    ds.append(_da)
    # endregion temp

    # region tsk
    print("Processing tsk...")
    _da = [wrf_getvar(wrf_outs, "TSK", t) for t in timeidxs]
    _da = xr.concat(_da, "time")
    _da = _da - 273.15
    _da.name = "tsk"
    ds.append(_da)
    # endregion tsk

    # region hi
    print("Processing heat index...")
    _da = [wrf_getvar(wrf_outs, "hi", t) for t in timeidxs]
    _da = xr.concat(_da, "time")
    _da.name = "hi"
    ds.append(_da)
    # endregion hi

    # region rh
    print("Processing 2m relative humidity...")
    _da = [wrf_getvar(wrf_outs, "rh2", t) for t in timeidxs]
    _da = xr.concat(_da, "time")
    _da.name = "rh"
    ds.append(_da)
    # endregion rh

    # region wind
    print("Processing wind...")
    u = [wrf_getvar(wrf_outs, "ua", t, levels=850, interp="pressure") for t in timeidxs]
    u = xr.concat(u, "time")
    u.name = "u_850hPa"
    u = u.drop("level")
    ds.append(u)
    v = [wrf_getvar(wrf_outs, "va", t, levels=850, interp="pressure") for t in timeidxs]
    v = xr.concat(v, "time")
    v.name = "v_850hPa"
    v = v.drop("level")
    ds.append(v)
    # endregion wind

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
    ds.append(_da)
    # endregion wpd

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
    ds.append(_da)
    # endregion ppv

    ds = xr.merge(ds)
    ds = ds.assign_coords(
        west_east=ds.lon[0, :].values,
        south_north=ds.lat[:, 0].values,
        time=[pd.to_datetime(dt) - timedelta(days=1) for dt in ds.time.values],
    )
    ds = ds.drop(["lon", "lat", "xtime"])
    ds = ds.rename({"west_east": "lon", "south_north": "lat", "key_0": "ens"})

    _out_dir = out_dir / "maps"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating maps...")
    plot_maps(ds, _out_dir)
    _out_dir = out_dir / "web/maps"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating web maps...")
    plot_web_maps(ds, _out_dir)
    _out_dir = out_dir / "web/json"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating summary...")
    extract_points(ds, _out_dir)


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
