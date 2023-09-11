import os
import warnings
from pathlib import Path
import pytz
from cartopy import crs as ccrs

from dataclasses import dataclass, field


@dataclass
class Config:
    tz: pytz.BaseTzInfo = field(init=False, default=pytz.timezone("Asia/Manila"))
    plot_proj: ccrs.PlateCarree = field(init=False, default=ccrs.PlateCarree())
    data_dir: Path = field(init=False)
    wrf_maindir: Path = field(init=False)
    script_dir: Path = field(init=False)
    wrf_forecast_days: int = field(init=False)
    wrf_run_names: list[str] = field(init=False)
    num_ens_member: int = field(init=False)
    wrf_dirs: list[Path] = field(init=False)

    def __post_init__(self):
        data_dir = os.getenv("OUTDIR")
        if data_dir is None:
            raise NotADirectoryError("OUTDIR not set")
        else:
            self.data_dir = Path(data_dir)

        wrf_maindir = os.getenv("WRF_REALDIR")
        if wrf_maindir is None:
            raise NotADirectoryError("WRF_REALDIR not set")
        else:
            self.wrf_maindir = Path(wrf_maindir)

        script_dir = os.getenv("SCRIPT_DIR")
        if script_dir is None:
            self.script_dir = wrf_maindir / "scripts"
            warnings.warn(f"SCRIPT_DIR not set, script_dir set to '{script_dir}'")
        else:
            self.script_dir = Path(script_dir)

        wrf_forecast_days = os.getenv("WRF_FCST_DAYS")
        if wrf_forecast_days is None:
            self.wrf_forecast_days = 3
            warnings.warn(
                f"WRF_FCST_DAYS not set, wrf_forecast_days set to '{wrf_forecast_days}'"
            )
        else:
            self.wrf_forecast_days = int(wrf_forecast_days)

        wrf_run_names = os.getenv("WRF_RUN_NAMES")
        if wrf_run_names is None:
            wrf_run_names = "run1:run2"
            warnings.warn(
                f"WRF_RUN_NAMES not set, wrf_run_names set to '{wrf_run_names}'"
            )
        self.wrf_run_names = wrf_run_names.split(":")
        self.wrf_dirs = [
            self.wrf_maindir / wrf_run_name for wrf_run_name in self.wrf_run_names
        ]

        self.num_ens_member = len(self.wrf_run_names)
