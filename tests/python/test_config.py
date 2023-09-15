import pytest
from config import Config


def test_config_default():
    with pytest.warns(UserWarning):
        conf = Config()
        assert str(conf.tz) == "Asia/Manila"
        assert str(conf.data_dir) == "output"
        assert str(conf.wrf_realdir) == "model/WRF"
        assert str(conf.script_dir) == "scripts"
        assert conf.wrf_forecast_days == 3
        for i, wrf_dir in enumerate(conf.wrf_dirs):
            assert wrf_dir.name == f"run{i+1}"


def test_config(monkeypatch):
    monkeypatch.setenv("OUTDIR", "forecast/output")
    monkeypatch.setenv("WRF_REALDIR", "forecast/model/WRF")
    monkeypatch.setenv("SCRIPT_DIR", "forecast/scripts")
    monkeypatch.setenv("WRF_FCST_DAYS", "5")
    monkeypatch.setenv("WRF_RUN_NAMES", "run1:run2:run3")

    conf = Config()
    assert str(conf.tz) == "Asia/Manila"
    assert str(conf.data_dir) == "forecast/output"
    assert str(conf.wrf_realdir) == "forecast/model/WRF"
    assert str(conf.script_dir) == "forecast/scripts"
    assert conf.wrf_forecast_days == 5
    for i, wrf_dir in enumerate(conf.wrf_dirs):
        assert wrf_dir.name == f"run{i+1}"
