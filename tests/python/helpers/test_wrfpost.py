import pytest
from pytest_mock import MockerFixture
from pathlib import Path

from config import Config

from helpers.wrfpost import get_hour_ds


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
