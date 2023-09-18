import pytest
from pytest_mock import MockerFixture
from pathlib import Path


from config import Config

from netCDF4 import Dataset
import xarray as xr

from helpers.wrfpost import (
    get_hour_ds,
    create_hour_ds,
    create_interval_ds,
    save_as_netcdf,
)


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


@pytest.mark.slow
@pytest.mark.parametrize(
    "num_ens, args",
    [
        (1, {}),
        (1, {"include_vars": ["u_850hPa", "v_850hPa"]}),
        (1, {"exclude_vars": ["wpd", "ppv", "ghi"]}),
        (2, {"include_vars": ["rain", "rh"]}),
        (3, {"include_vars": ["wpd"]}),
    ],
)
def test_create_hour_ds(monkeypatch, tmp_path, wrfout: Path, num_ens: int, args):
    monkeypatch.setenv("OUTDIR", str(tmp_path / "output"))
    monkeypatch.setenv("WRF_REALDIR", str(tmp_path / "model/wrf"))
    monkeypatch.setenv("WRF_RUN_NAMES", "run1")
    monkeypatch.setenv("WRF_FCST_DAYS", "1")

    wrfin = {}
    for n in range(num_ens):
        wrfin[f"ens{n}"] = Dataset(wrfout)
    if wrfout is not None:
        hr_ds = create_hour_ds(wrfin, **args)
        assert isinstance(hr_ds, xr.Dataset)
        for dim in ["time", "lat", "lon"]:
            assert dim in hr_ds.dims
        if num_ens == 1:
            assert "ens" not in hr_ds.dims
        elif num_ens > 1:
            assert "ens" in hr_ds.dims
        if "include_vars" in args:
            for var_name in args["include_vars"]:
                assert var_name in hr_ds.variables
        if "exclude_vars" in args:
            for var_name in args["exclude_vars"]:
                assert var_name not in hr_ds.variables


@pytest.mark.slow
@pytest.mark.parametrize(
    "hr_interval",
    [24, 3],
)
def test_create_interval_ds(monkeypatch, tmp_path, wrfnc: Path, hr_interval: int):
    monkeypatch.setenv("OUTDIR", str(tmp_path / "output"))
    monkeypatch.setenv("WRF_REALDIR", str(tmp_path / "model/wrf"))
    monkeypatch.setenv("SCRIPT_DIR", str(tmp_path / "scripts"))
    monkeypatch.setenv("WRF_FCST_DAYS", "1")

    hr_ds = xr.open_dataset(wrfnc)
    ds = create_interval_ds(hr_ds, hr_interval)
    assert isinstance(ds, xr.Dataset)
    assert not (set(hr_ds.keys()) ^ set(ds.keys()))
    assert hr_ds.time.shape[0] > ds.time.shape[0]


def test_save_as_netcdf(mocker: MockerFixture):
    m_dataset = mocker.patch("xarray.Dataset")
    ds = m_dataset()
    out_file = Path("tmp")
    save_as_netcdf(ds, out_file)
    assert ds.lon.attrs.__setitem__.call_count > 1
    assert ds.lat.attrs.__setitem__.call_count > 1
    ds.to_netcdf.assert_called_once_with(out_file, unlimited_dims=["time"])
