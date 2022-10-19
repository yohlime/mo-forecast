from typing import List
from pathlib import Path
from tqdm import tqdm
from datetime import timedelta
import pandas as pd
import xarray as xr

from __const__ import wrf_forecast_days, data_dir

from helpers.wrf import wrf_getvar

VARS = {
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


def get_hour_ds(date_str: str = "", src_dir: Path = data_dir / "nc") -> xr.Dataset:
    """Retrieve hourly dataset from post-processed WRF output

    Args:
        date_str (str, optional): Date string in `%Y-%m-%d_%H` format. Defaults to "".
        src_dir (str or Path, optional): Source directory. Defaults to data_dir/"nc".

    Returns:
        xr.Dataset or None: hourly Dataset
    """
    if not isinstance(src_dir, Path):
        src_dir = Path(src_dir)

    if date_str != "":
        files = list(src_dir.glob(f"*{date_str}.nc"))
    else:
        files = sorted(src_dir.glob("*.nc"), reverse=True)

    if len(files) == 0:
        print("File not found")
        return None

    return xr.open_dataset(files[0])


def create_hour_ds(
    wrfin,
    include_vars: List[str] = None,
    exclude_vars: List[str] = None,
) -> xr.Dataset:
    """Create hourly dataset from WRF-ARW netCDF data

    Args:
        wrfin (netCDF4.Dataset, Nio.NioFile, or an iterable): WRF-ARW netCDF
            data as a netCDF4.Dataset, Nio.NioFile or an iterable sequence of
            the aforementioned types.
        include_vars (List[str], optional): Variables to include.
            Defaults to including all variables.
        exclude_vars (List[str], optional): Variables to exclude. Defaults to None.

    Returns:
        xr.Dataset: hourly Dataset
    """
    nt = wrf_forecast_days * 24 + 1
    hr_ds = []

    _vars = VARS.copy()
    if include_vars and isinstance(include_vars, list):
        _vars = {k: v for k, v in VARS.items() if k in include_vars}
    elif exclude_vars and isinstance(exclude_vars, list):
        _vars = {k: v for k, v in VARS.items() if k not in exclude_vars}

    # process needed variables
    for var_name, var_info in tqdm(_vars.items(), total=len(_vars)):
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
    return hr_ds


def create_interval_ds(hr_ds: xr.Dataset, hr_interval) -> xr.Dataset:
    """Create daily dataset from processed hourly data

    Args:
        hr_ds (xr.Dataset): processed WRF hourly data

    Returns:
        xr.Dataset: daily Dataset
    """
    var_names = list(hr_ds.keys())
    interval_range = range(1, wrf_forecast_days * 24 // hr_interval + 1)
    intervalidxs = [interval * hr_interval for interval in interval_range]
    interval_ds = []

    instant_var_names = ["temp", "tsk", "hi", "rh", "u_850hPa", "v_850hPa"]
    sum_var_names = ["rain", "wpd", "ppv", "ghi"]
    max_var_names = ["hix"]

    _var_names = [v for v in var_names if v in instant_var_names]
    if _var_names:
        _ds = hr_ds[_var_names].isel(time=intervalidxs).copy()
        _ds = _ds.assign_coords(
            time=[
                pd.to_datetime(dt) - timedelta(hours=hr_interval)
                for dt in _ds.time.values
            ],
        )
        interval_ds.append(_ds)

    _var_names = [v for v in var_names if v in sum_var_names]
    if _var_names:
        init_dt = pd.to_datetime(hr_ds.time.values[0])
        _ds = hr_ds[_var_names].sel(time=hr_ds.time[1:]).copy()
        _ds = _ds.assign_coords(
            time=[
                pd.to_datetime(dt) - timedelta(hours=init_dt.hour + 1)
                for dt in _ds.time.values
            ],
        )
        _ds = _ds.resample(time=f"{hr_interval}H").sum("time")
        _ds = _ds.assign_coords(
            time=interval_ds[0].time.values,
        )
        interval_ds.append(_ds)

    _var_names = [v for v in var_names if v in max_var_names]
    if _var_names:
        init_dt = pd.to_datetime(hr_ds.time.values[0])
        _ds = hr_ds[_var_names].sel(time=hr_ds.time[1:]).copy()
        _ds = _ds.assign_coords(
            time=[
                pd.to_datetime(dt) - timedelta(hours=init_dt.hour + 1)
                for dt in _ds.time.values
            ],
        )
        _ds = _ds.resample(time=f"{hr_interval}H").max("time")
        _ds = _ds.assign_coords(
            time=interval_ds[0].time.values,
        )
        interval_ds.append(_ds)

    return xr.merge(interval_ds)


def save_to_netcdf(ds: xr.Dataset, out_file: Path):
    """Save as netCDF file

    Args:
        ds (xr.Dataset): input data
        out_file (Path): file path
    """
    ds.lon.attrs["units"] = "degrees_east"
    ds.lon.attrs["standard_name"] = "longitude"
    ds.lon.attrs["long_name"] = "longitude"
    ds.lat.attrs["units"] = "degrees_north"
    ds.lat.attrs["standard_name"] = "latitude"
    ds.lat.attrs["long_name"] = "latitude"
    ds.to_netcdf(out_file, unlimited_dims=["time"])
