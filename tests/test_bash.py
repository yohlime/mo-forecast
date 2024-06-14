import os
from pathlib import Path
from datetime import datetime, timedelta


def test_wps(run_script, set_date_env):
    ts = datetime(2024, 6, 3, 12)
    set_date_env(ts)

    result = run_script("run_wps.sh")
    assert result.returncode == 0

    wrf_maindir = os.getenv("WRF_MAINDIR")
    namelist_suff = os.getenv("NAMELIST_SUFF")
    assert wrf_maindir is not None
    namelist = Path(wrf_maindir) / f"WPS/namelist.wps_{namelist_suff}"
    assert namelist.exists()

    with open(str(namelist), "r") as file:
        lines = file.readlines()

    assert len(lines) >= 5
    assert f"{ts:%Y-%m-%d_%H:00:00}" in lines[3].strip()

    ndays = os.getenv("WRF_FCST_DAYS")
    assert ndays is not None
    ts2 = ts + timedelta(days=int(ndays))
    assert f"{ts2:%Y-%m-%d_%H:00:00}" in lines[4].strip()


def test_wrf(run_script, set_date_env, create_met_ems):
    ts = datetime(2024, 6, 3, 12)
    set_date_env(ts)

    create_met_ems()
    result = run_script("run_wrf.sh")
    assert result.returncode == 0

    wrf_realdir = os.getenv("WRF_REALDIR")
    namelist_run = os.getenv("NAMELIST_RUN")
    assert wrf_realdir is not None
    namelist = Path(wrf_realdir) / f"namelist.input_{namelist_run}"
    assert namelist.exists()

    with open(str(namelist), "r") as file:
        lines = file.readlines()

    assert len(lines) >= 15

    ndays = os.getenv("WRF_FCST_DAYS")
    assert ndays is not None

    assert ndays in lines[1].strip()
    assert f"{ts:%Y}" in lines[5].strip()
    assert f"{ts:%m}" in lines[6].strip()
    assert f"{ts:%d}" in lines[7].strip()
    assert f"{ts:%H}" in lines[8].strip()
    ts2 = ts + timedelta(days=int(ndays))
    assert f"{ts2:%Y}" in lines[11].strip()
    assert f"{ts2:%m}" in lines[12].strip()
    assert f"{ts2:%d}" in lines[13].strip()
    assert f"{ts2:%H}" in lines[14].strip()
