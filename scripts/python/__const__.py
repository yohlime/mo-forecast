import os
from pathlib import Path
import seaborn as sns

wrf_forecast_days = int(os.getenv("WRF_FCST_DAYS"))
wrf_maindir = Path(os.getenv("WRF_REALDIR"))
wrf_run_names = os.getenv("WRF_RUN_NAMES").split(":")
wrf_dirs = [wrf_maindir / wrf_run_name for wrf_run_name in wrf_run_names]

script_dir = Path(os.getenv("SCRIPT_DIR"))


num_ens_member = len(wrf_run_names)

plot_vars = {
    "rain": {
        "title": "24-Hr Total Rainfall [mm]",
        "units": "mm",
        "levels": [5, 10, 20, 30, 50, 100, 150, 200, 250],
        "colors": [
            "#ffffff",
            "#0064ff",
            "#01b4ff",
            "#32db80",
            "#9beb4a",
            "#ffeb00",
            "#ffb302",
            "#ff6400",
            "#eb1e00",
            "#af0000",
        ],
    },
    "temp": {
        "title": "Air (2m) and Sea Surface Temperature [°C]",
        "units": "°C",
        "levels": range(20, 42, 2),
        "colors": sns.blend_palette(
            ["#f0e68c", "#ff4500", "#9932cc", "#000000"], n_colors=12
        ),
    },
    "hi": {
        "title": "Heat Index [°C]",
        "units": "°C",
        "levels": [27, 32, 41, 54],
        "colors": sns.blend_palette(
            ["#ffffff", "#f0e68c", "#ff8c00", "#b22222", "#9932cc"], n_colors=5
        ),
    },
    "rh": {
        "title": "Relative Humidity (2m)[%]",
        "units": "%",
        "levels": range(30, 110, 10),
        "colors": sns.blend_palette(
            [
                "#d7191c",
                "#fdae61",
                "#ffffbf",
                "#abdda4",
                "#2b83ba",
            ],
            n_colors=9,
        ),
    },
    "wind": {
        "title": "Winds (850mb)[m/s]",
        "units": "m/s",
        "levels": range(10, 70, 10),
        "colors": [(0, 0, 0)]
        + sns.blend_palette(
            [
                "#2b83ba",
                "#abdda4",
                "#ffffbf",
                "#fdae61",
                "#d7191c",
            ],
            n_colors=6,
        ),
    },
    "wpd": {
        "title": "24-Hr Total Wind Power Potential [MW]",
        "units": "MW",
        "levels": [2.1, 3.2, 4.2, 5.2, 6.2, 8.3],
        "colors": [
            "#ffffff",
            "#ffb302",
            "#ffeb00",
            "#9beb4a",
            "#32db80",
            "#01b4ff",
            "#0064ff",
            "#000096",
        ],
    },
    "ppv": {
        "title": "24-Hr Total Solar Power Potential [MW]",
        "units": "MW",
        "levels": [1, 2.4, 3.8, 5.2, 6.6, 8],
        "colors": sns.blend_palette(
            [
                "#66cdaa",
                "#f0e68c",
                "#ff8c00",
                "#b22222",
            ],
            n_colors=7,
        ),
    },
}

plot_vars_web = {
    "wpd": {
        "levels": [2.1, 3.2, 4.2, 5.2, 6.2, 8.3],
        "colors": [
            "#ffffff",
            "#ffb302",
            "#ffeb00",
            "#9beb4a",
            "#32db80",
            "#01b4ff",
            "#0064ff",
            "#000096",
        ],
    },
    "ppv": {
        "levels": [1, 2.4, 3.8, 5.2, 6.6, 8],
        "colors": sns.blend_palette(
            [
                "#66cdaa",
                "#f0e68c",
                "#ff8c00",
                "#b22222",
            ],
            n_colors=7,
        ),
    },
    "temp": {
        "levels": range(20, 42, 2),
        "colors": sns.blend_palette(
            ["#f0e68c", "#ff4500", "#9932cc", "#000000"], n_colors=12
        ),
    },
    "rainchance": {
        "levels": [i / 3 for i in range(num_ens_member + 1)],
        "colors": ["#ffffff"]
        + sns.blend_palette(
            [
                "#b0e0e6",
                "#1e90ff",
                "#000080",
            ],
            n_colors=num_ens_member,
        ),
    },
    "wind": {
        "levels": range(10, 70, 10),
        "colors": sns.color_palette(
            "RdPu",
            n_colors=7,
        ),
    },
}
