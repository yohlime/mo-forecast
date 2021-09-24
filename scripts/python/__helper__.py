import numpy as np
from wrf import getvar, interplevel
import metpy.calc as mpcalc
from metpy.units import units


def wrf_getvar(wrfin, varname, timeidx=0, levels=None, interp=None):
    """Wrapper around wrf-python's getvar

    Args:
        wrfin (`netCDF4.Dataset`, `Nio.NioFile`, or an iterable): WRF-ARW NetCDF
            data as a `netCDF4.Dataset`, `Nio.NioFile` or an iterable sequence of
            the aforementioned types.
        varname (str): The variable name
        timeidx (int, optional): The desired time index. Defaults to 0.
        levels (List[float] or `numpy.ndarray`, optional): Desired levels.
            Defaults to None.
        interp (str, optional): Type of vertical interpolation. Defaults to None.

    Returns:
        If xarray is enabled and the meta parameter is True, then the result will be a
        `xarray.DataArray` object. Otherwise, the result will be a `numpy.ndarray`
        object with no metadata.
    """
    if varname == "prcp":
        da = getvar(wrfin, "RAINC", timeidx) + getvar(wrfin, "RAINNC", timeidx).values
        da.name = "prcp"
    elif varname == "hi":
        t = getvar(wrfin, "T2", timeidx) - 273.15
        rh = getvar(wrfin, "rh2", timeidx)
        da = heat_index(t, rh)
        da.name = "hi"
    elif varname == "wpd":
        # wspd = wrf_getvar(wrfin, "wspd_wdir", timeidx, levels=80, interp="height_agl")[
        #     0, :
        # ]
        u = wrf_getvar(wrfin, "ua", timeidx, levels=80, interp="height_agl")
        v = wrf_getvar(wrfin, "va", timeidx, levels=80, interp="height_agl")
        wspd = u.copy()
        wspd.values = (u.values ** 2 + v.values ** 2) ** 0.5
        da = wind_power_density(wspd)
        da.name = "wpd"
    elif varname == "ppv":
        swddni = getvar(wrfin, "SWDDNI", timeidx)
        coszen = getvar(wrfin, "COSZEN", timeidx)
        swddif = getvar(wrfin, "SWDDIF", timeidx)
        t = getvar(wrfin, "T2", timeidx) - 273.15
        da = pv_power_potential(swddni, coszen, swddif, t)
        da.name = "ppv"
    else:
        da = getvar(wrfin, varname, timeidx)

    if levels is not None:
        if interp in ["pressure", "height", "height_agl"]:
            vert = getvar(wrfin, interp, timeidx)
        da = interplevel(da, vert, levels)

    tr = {"Time": "time", "XLAT": "lat", "XLONG": "lon", "XTIME": "xtime"}
    tr = {k: tr[k] for k in tr.keys() if k in da.coords}
    da = da.rename(tr)
    return da


def heat_index(t, rh):
    """Computes Heat Index based on Rothfusz (1990).

    Args:
        t (xarray.DataArray): Air Temperature in °C
        rh (xarray.DataArray): Relative Humidity

    Returns:
        xarray.DataArray: Heat Index in °C
    """
    _t = t * units.degC
    _rh = rh * units.percent
    hi = mpcalc.heat_index(
        _t,
        _rh,
    )
    return hi.metpy.convert_units(units.degC).metpy.dequantify()


def wind_power_density(wspd):
    """Computes wind power density

    Args:
        wspd (xarray.DataArray): Wind speed in m/s

    Returns:
        xarray.DataArray: Wind Power Density in MW
    """
    a = 0.5  # constant
    rho = 1.23  # air density
    # r = 52  # blade length of turbine (radius)
    cp = 0.4  # power coefficient
    # cf = 0.4  # cf = capacity factor (40%)
    turb = 4  # assume 4 wind turbines in one hectare
    swarea = 8495  # swept area of turbine

    wpd = turb * (a * rho * swarea * cp * wspd ** 3)
    return wpd / 1000000


def pv_power_potential(swddni, coszen, swddif, t):
    """Computes PV Power Potential

    Args:
        swddni (xarray.DataArray): [description]
        coszen (xarray.DataArray): [description]
        swddif (xarray.DataArray): [description]
        t (xarray.DataArray): 2m Air temperature in °C

    Returns:
        xarray.DataArray: [description]
    """
    c1 = -3.75
    c2 = 1.14
    c3 = 0.0175
    beta = 0.0045
    gamma = 0.1
    t_ref = 25.0
    eta_ref = 0.12

    ghi = (swddni * coszen.values) + swddif.values
    t_cell = c1 + c2 * t + c3 * ghi.values
    eta_cell = eta_ref * (1 - beta * (t_cell - t_ref) + gamma * np.log10(ghi.values))
    ppv = ghi * eta_cell.values

    # adjust to number of solar panels in 1 hectare = 7200
    # adjust to MW
    spanel = 7200
    # cf = 0.2
    return ppv * spanel / 1000000
