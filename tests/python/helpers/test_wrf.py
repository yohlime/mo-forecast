import pytest
from pytest_mock import MockerFixture
from pathlib import Path

import netCDF4 as nc4
import xarray as xr

from helpers.wrf import get_required_variables, create_wrfout_subset, wrf_getvar


@pytest.mark.parametrize(
    "var_name, var_list, has_warning",
    [
        ("RAINC", ("RAINC",), False),
        ("prcp", ("RAINC", "RAINNC"), False),
        ("hi", ("T2", "PSFC", "Q2"), False),
        ("v_80m", ("V", "P", "PH", "PHB", "HGT"), False),
        ("u_850hPa", ("U", "P", "PB"), False),
        ("random", [], True),
    ],
)
def test_get_required_variables(var_name, var_list, has_warning):
    if has_warning:
        with pytest.warns(UserWarning):
            assert len(get_required_variables(var_name)) == 0
    else:
        assert not set(get_required_variables(var_name)) ^ set(var_list)


@pytest.mark.parametrize(
    "args",
    [
        ("wrfout_sample", "wrfout_subset_sample"),
        ("wrfout_sample", "wrfout_subset_sample", ["var1", "var2"]),
        ("wrfout_sample", "wrfout_subset_sample", None, ["var1", "var2"]),
        ("wrfout_sample", "wrfout_subset_sample", None, None, True),
    ],
)
def test_create_wrfout_subset(mocker: MockerFixture, args):
    m_open_dataset = mocker.patch("xarray.open_dataset")
    m_path_unlink = mocker.patch.object(Path, "unlink", return_value=True)
    m_get_required_variables = mocker.patch("helpers.wrf.get_required_variables")

    create_wrfout_subset(*args)
    m_open_dataset.assert_called_once_with(args[0])
    if (len(args) >= 3) and args[2] is not None:
        c_args = m_open_dataset().__getitem__.call_args.args[0]
        assert set(args[2]).issubset(set(c_args))
    if (len(args) >= 4) and args[3] is not None:
        m_get_required_variables.assert_called()
    else:
        m_get_required_variables.assert_not_called()
    if (len(args) == 5) and args[4]:
        m_path_unlink.assert_called_once()
    m_open_dataset().__getitem__().to_netcdf.assert_called_once_with(Path(args[1]))


@pytest.mark.parametrize(
    "num_ens, args",
    [
        (1, {"varname": "T2"}),
        (1, {"varname": "prcp"}),
        (3, {"varname": "T2"}),
        (3, {"varname": "prcp"}),
        (2, {"varname": "hi"}),
        (
            2,
            {
                "varname": "ua",
                "levels": 850,
                "interp": "pressure",
            },
        ),
        (
            2,
            {
                "varname": "va",
                "levels": 850,
                "interp": "pressure",
            },
        ),
        (2, {"varname": "wpd"}),
        (2, {"varname": "ppv"}),
        (2, {"varname": "ghi"}),
    ],
)
def test_wrf_getvar(mocker, wrfout, num_ens, args):
    wrfin = {}
    for n in range(num_ens):
        wrfin[f"ens{n}"] = nc4.Dataset(wrfout)
    if wrfout is not None:
        wrf_var = wrf_getvar(wrfin, **args)
        assert isinstance(wrf_var, xr.DataArray)
        for dim in ["time", "south_north", "west_east"]:
            assert dim in wrf_var.dims
        if num_ens == 1:
            assert "ens" not in wrf_var.dims
        elif num_ens > 1:
            assert "ens" in wrf_var.dims
