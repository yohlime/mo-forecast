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
from plot_ts import plot_timeseries
from plot_web_maps import plot_web_maps
from extract_points import extract_points


omp_set_num_threads(int(os.getenv("SLURM_NTASKS", 4)))
print(f"Using {omp_get_max_threads()} threads...")

tz = pytz.timezone("Asia/Manila")


def main(wrf_outs, out_dir):
    dayidxs = [day * 24 for day in range(1, wrf_forecast_days + 1)]

    hr_ds = []

    # region rain
    print("Processing rain...")
    _da = wrf_getvar(wrf_outs, "prcp", None)
    __da = []
    for i in range(_da.time.shape[0]):
        if i > 0:
            d = _da.isel(time=i)
            d.values = d.values - _da.isel(time=(i - 1)).values
            __da.append(d)
        else:
            __da.append(_da.isel(time=i))
    _da = xr.concat(__da, "time")
    _da = _da.transpose("key_0", "time", ...)
    _da.name = "rain"
    hr_ds.append(xr.DataArray(_da, attrs={}))
    # endregion rain

    # region temp
    print("Processing 2m temperature...")
    _da = wrf_getvar(wrf_outs, "T2", None)
    _da = _da - 273.15
    _da.name = "temp"
    hr_ds.append(xr.DataArray(_da, attrs={}))
    # endregion temp

    # region tsk
    print("Processing tsk...")
    _da = wrf_getvar(wrf_outs, "TSK", None)
    _da = _da - 273.15
    _da.name = "tsk"
    hr_ds.append(xr.DataArray(_da, attrs={}))
    # endregion tsk

    # region hi
    print("Processing heat index...")
    _da = wrf_getvar(wrf_outs, "hi", None)
    _da.name = "hi"
    hr_ds.append(xr.DataArray(_da, attrs={}))
    # endregion hi

    # region rh
    print("Processing 2m relative humidity...")
    _da = wrf_getvar(wrf_outs, "rh2", None)
    _da.name = "rh"
    hr_ds.append(xr.DataArray(_da, attrs={}))
    # endregion rh

    # region wind
    print("Processing wind...")
    u = [
        wrf_getvar(wrf_outs, "ua", t, levels=850, interp="pressure")
        for t in range(hr_ds[0].shape[1])
    ]
    u = xr.concat(u, "time")
    u = u.transpose("key_0", "time", ...)
    u.name = "u_850hPa"
    u = u.drop("level")
    hr_ds.append(xr.DataArray(u, attrs={}))
    v = [
        wrf_getvar(wrf_outs, "va", t, levels=850, interp="pressure")
        for t in range(hr_ds[0].shape[1])
    ]
    v = xr.concat(v, "time")
    v = v.transpose("key_0", "time", ...)
    v.name = "v_850hPa"
    v = v.drop("level")
    hr_ds.append(xr.DataArray(v, attrs={}))
    # endregion wind

    # region wpd
    print("Processing wpd...")
    _da = [wrf_getvar(wrf_outs, "wpd", t) for t in range(hr_ds[0].shape[1])]
    _da = xr.concat(_da, "time")
    _da = _da.transpose("key_0", "time", ...)
    _da = _da.drop(["level", "wspd_wdir"])
    hr_ds.append(xr.DataArray(_da, attrs={}))
    # endregion wpd

    # region ppv
    print("Processing ppv...")
    _da = wrf_getvar(wrf_outs, "ppv", None)
    hr_ds.append(xr.DataArray(_da, attrs={}))
    # endregion ppv

    hr_ds = xr.merge(hr_ds)
    hr_ds = hr_ds.assign_coords(
        west_east=hr_ds.lon[0, :].values,
        south_north=hr_ds.lat[:, 0].values,
        key_0=range(len(wrf_outs)),
    )
    hr_ds = hr_ds.drop(["lon", "lat", "xtime"])
    hr_ds = hr_ds.rename({"west_east": "lon", "south_north": "lat", "key_0": "ens"})

    day_ds = []

    _ds = (
        hr_ds[["temp", "tsk", "hi", "rh", "u_850hPa", "v_850hPa"]]
        .isel(time=dayidxs)
        .copy()
    )
    _ds = _ds.assign_coords(
        time=[pd.to_datetime(dt) - timedelta(days=1) for dt in _ds.time.values],
    )
    day_ds.append(_ds)
    _ds = hr_ds[["rain", "wpd", "ppv"]].sel(time=hr_ds.time[1:]).copy()
    _ds = _ds.assign_coords(
        time=[pd.to_datetime(dt) - timedelta(hours=1) for dt in _ds.time.values],
    )
    _ds = _ds.groupby("time.day").sum().rename({"day": "time"})
    _ds = _ds.assign_coords(
        time=day_ds[0].time.values,
    )
    day_ds.append(_ds)
    day_ds = xr.merge(day_ds)

    _out_dir = out_dir / "maps"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating maps...")
    plot_maps(day_ds, _out_dir)

    _out_dir = out_dir / "timeseries"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating ts plot...")
    plot_timeseries(hr_ds, _out_dir)

    _out_dir = out_dir / "web/maps"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating web maps...")
    plot_web_maps(day_ds, _out_dir)

    _out_dir = out_dir / "web/json"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating summary...")
    extract_points({"hr": hr_ds, "day": day_ds}, _out_dir)

    print("Saving nc...")
    init_dt = pd.to_datetime(hr_ds.time.values[0])
    init_dt_str = init_dt.strftime("%Y-%m-%d_%H")
    out_file = out_dir / f"nc/wrf_{init_dt_str}.nc"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    hr_ds.to_netcdf(out_file, unlimited_dims=["time"])


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
