import os
import sys
import getopt
from tqdm import tqdm
from pathlib import Path
from datetime import timedelta
from netCDF4 import Dataset
import pandas as pd
import xarray as xr
import pytz

from wrf import omp_set_num_threads, omp_get_max_threads

from __const__ import wrf_dirs, wrf_forecast_days
from helpers.wrf import wrf_getvar
from plot_maps import plot_maps
from plot_ts import plot_timeseries
from plot_web_maps import plot_web_maps
from extract_points import extract_points
from plot_hi_gauge import plot_gauge
from plot_ari_maps import plot_ari
from extract_acenergy import extract_acenergy
from extract_points_for_validation import extract_points_for_validation
from plot_ts_acenergy import plot_ts_ace

omp_set_num_threads(int(os.getenv("SLURM_NTASKS", 4)))
print(f"Using {omp_get_max_threads()} threads...")

tz = pytz.timezone("Asia/Manila")

vars = {
    "rain": {"varname": "prcp"},
    "temp": {"varname": "T2"},
    "tsk": {"varname": "TSK"},
    "hi": {"varname": "hi"},
    "hix": {"varname": "hi"},
    "rh": {"varname": "rh2"},
    "u_850hPa": {"varname": "ua", "levels": 850, "interp": "pressure"},
    "v_850hPa": {"varname": "va", "levels": 850, "interp": "pressure"},
    "wpd": {"varname": "wpd"},
    "ppv": {"varname": "ppv"},
    "ghi": {"varname": "ghi"},
}


def main(wrfin, out_dir):
    nt = wrf_forecast_days * 24 + 1

    # region create hourly dataset
    hr_ds = []

    # process needed variables
    for var_name, var_info in tqdm(vars.items(), total=len(vars)):
        print(f"Processing {var_name}...")
        if var_name == "rain":
            _da = wrf_getvar(wrfin, timeidx=None, **var_info)
            # create step-wise values
            __da = []
            for i in range(nt):
                if i > 0:
                    d = _da.isel(time=i)
                    d.values = d.values - _da.isel(time=(i - 1)).values
                    __da.append(d)
                else:
                    __da.append(_da.isel(time=i))
            _da = __da.copy()
        elif var_name in ["u_850hPa", "v_850hPa"]:
            _da = [wrf_getvar(wrfin, timeidx=t, **var_info) for t in range(nt)]
        elif var_name in ["wpd"]:
            _da = [wrf_getvar(wrfin, timeidx=t, **var_info) for t in range(nt)]
        else:
            _da = wrf_getvar(wrfin, timeidx=None, **var_info)

        if var_name in ["temp", "tsk"]:
            _da = _da - 273.15  # K to degC

        if var_name in ["rain", "u_850hPa", "v_850hPa", "wpd"]:
            _da = xr.concat(_da, "time")
            _da = _da.transpose("key_0", "time", ...)

        if var_name in ["u_850hPa", "v_850hPa", "wpd"]:
            _da = _da.drop("level")

        _da.name = var_name
        hr_ds.append(xr.DataArray(_da, attrs={}))

    # merge to one xarrray.Dataset
    # clean coordinates/dims
    hr_ds = xr.merge(hr_ds)
    hr_ds = hr_ds.assign_coords(
        west_east=hr_ds.lon[0, :].values,
        south_north=hr_ds.lat[:, 0].values,
        key_0=range(len(wrfin.keys())),
    )
    hr_ds = hr_ds.drop(["lon", "lat", "xtime"])
    hr_ds = hr_ds.rename({"west_east": "lon", "south_north": "lat", "key_0": "ens"})
    # endregion create hourly dataset

    # region create daily dataset
    dayidxs = [day * 24 for day in range(1, wrf_forecast_days + 1)]
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

    init_dt = pd.to_datetime(hr_ds.time.values[0])
    _ds = hr_ds[["rain", "wpd", "ppv", "ghi"]].sel(time=hr_ds.time[1:]).copy()
    _ds = _ds.assign_coords(
        time=[
            pd.to_datetime(dt) - timedelta(hours=init_dt.hour + 1)
            for dt in _ds.time.values
        ],
    )
    _ds = _ds.groupby("time.day").sum().rename({"day": "time"})
    _ds = _ds.assign_coords(
        time=day_ds[0].time.values,
    )
    day_ds.append(_ds)

    init_dt = pd.to_datetime(hr_ds.time.values[0])
    _ds = hr_ds[["hix"]].sel(time=hr_ds.time[1:]).copy()
    _ds = _ds.assign_coords(
        time=[
            pd.to_datetime(dt) - timedelta(hours=init_dt.hour + 1)
            for dt in _ds.time.values
        ],
    )
    _ds = _ds.groupby("time.day").max().rename({"day": "time"})
    _ds = _ds.assign_coords(
        time=day_ds[0].time.values,
    )
    day_ds.append(_ds)

    day_ds = xr.merge(day_ds)
    # endregion create daily dataset

    # region output
    _out_dir = out_dir / "maps"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating maps...")
    plot_maps(day_ds, _out_dir)

    _out_dir = out_dir / "timeseries/img"
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

    _out_dir = out_dir / f"hi_gauge/img/{init_dt.strftime('%Y%m%d%H')}"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating HI gauge plots...")
    plot_gauge(hr_ds, _out_dir)

    _out_dir = out_dir / f"ari/img/{init_dt.strftime('%Y%m%d%H')}"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating ARI plots...")
    plot_ari(day_ds, _out_dir)

    _out_dir = out_dir / "acenergy/csv"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating summary for AC Energy solar farms...")
    extract_acenergy(hr_ds, _out_dir)

    _out_dir = out_dir / "acenergy/img"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating ts plot for AC Energy solar farms...")
    plot_ts_ace(hr_ds, _out_dir)

    _out_dir = out_dir / "stations_fcst_for_validation/json"
    _out_dir.mkdir(parents=True, exist_ok=True)
    print("Creating summary for stations for validation...")
    extract_points_for_validation({"hr": hr_ds, "day": day_ds}, _out_dir)

    print("Saving nc...")
    init_dt = pd.to_datetime(hr_ds.time.values[0])
    init_dt_str = init_dt.strftime("%Y-%m-%d_%H")
    out_file = out_dir / f"nc/wrf_{init_dt_str}.nc"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    hr_ds.lon.attrs["units"] = "degrees_east"
    hr_ds.lon.attrs["standard_name"] = "longitude"  # Optional
    hr_ds.lon.attrs["long_name"] = "longitude"
    hr_ds.lat.attrs["units"] = "degrees_north"
    hr_ds.lat.attrs["standard_name"] = "latitude"  # Optional
    hr_ds.lat.attrs["long_name"] = "latitude"
    hr_ds.to_netcdf(out_file, unlimited_dims=["time"])
    # endregion output


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
    wrfin = {f"ens{i}": Dataset(d / wrf_out) for i, d in enumerate(wrf_dirs)}
    main(wrfin, out_dir)
