import pytest
from pytest_mock import MockerFixture
from pathlib import Path


from config import Config

from helpers.wrfpost import (
    get_required_variables,
    create_wrfout_subset,
    get_hour_ds,
)


@pytest.mark.parametrize(
    "var_name, var_list",
    [
        ("rain", ["RAINC", "RAINNC"]),
        ("hi", ["T2", "PSFC", "Q2"]),
        ("v_80m", ["V", "P", "PH", "PHB", "HGT"]),
        ("u_850hPa", ["U", "P", "PB"]),
        ("random", ["random"]),
    ],
)
def test_get_required_variables(var_name, var_list):
    diff = set(get_required_variables(var_name)) ^ set(var_list)
    assert not diff


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
    m_get_required_variables = mocker.patch("helpers.wrfpost.get_required_variables")

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
    "date_str, src_dir, files, expected_output",
    [
        ("2023-01-01_00", None, ["file1.nc", "file2.nc"], "file1.nc"),
        ("2023-01-01_00", "src_dir", ["file1.nc", "file2.nc"], "file1.nc"),
        ("2023-01-01_00", Path("src_dir"), ["file1.nc", "file2.nc"], "file1.nc"),
        ("2023-01-01_00", Path("src_dir"), [], None),
    ],
)
def test_get_hour_ds(mocker: MockerFixture, date_str, src_dir, files, expected_output):
    mocker.patch.object(Path, "glob", return_value=files)
    ret_val = None
    if len(files):
        ret_val = files[0]
    m_open_dataset = mocker.patch("xarray.open_dataset", return_value=ret_val)
    if src_dir is None:
        mocker.patch.object(Config, "__post_init__")
        mocker.patch.object(Config, "data_dir", Path("sample_dir"), create=True)
    assert get_hour_ds(date_str, src_dir) == expected_output
    if len(files):
        m_open_dataset.assert_called_once_with(ret_val)
