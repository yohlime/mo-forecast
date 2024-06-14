import pytest
from config import Config


def test_config_default(monkeypatch):
    monkeypatch.undo()
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
    outdir = "forecast/output"
    wrf_realdir = "forecast/model/WRF"
    script_dir = "forecast/scripts"
    ndays = 17
    run_names = ("run1", "xrun33", "walk85", "simbest")

    monkeypatch.setenv("OUTDIR", outdir)
    monkeypatch.setenv("WRF_REALDIR", wrf_realdir)
    monkeypatch.setenv("SCRIPT_DIR", script_dir)
    monkeypatch.setenv("WRF_FCST_DAYS", f"{ndays}")
    monkeypatch.setenv("WRF_RUN_NAMES", ":".join(run_names))

    conf = Config()
    assert str(conf.tz) == "Asia/Manila"
    assert str(conf.data_dir) == outdir
    assert str(conf.wrf_realdir) == wrf_realdir
    assert str(conf.script_dir) == script_dir
    assert conf.wrf_forecast_days == ndays
    for i, wrf_dir in enumerate(conf.wrf_dirs):
        assert wrf_dir.name == run_names[i]
