import sys
import getopt
from pathlib import Path
import pandas as pd
import xarray as xr
from salem import open_xr_dataset
from cartopy import crs as ccrs
import pytz

import matplotlib.pyplot as plt

from wrf import omp_set_num_threads, omp_get_max_threads

from __const__ import wrf_dirs, plot_vars_web, script_dir
from __helper__ import wrf_getvar, wrf_getproj


omp_set_num_threads(omp_get_max_threads())
print(f"Using {omp_get_max_threads()} threads...")

# ph_gdf = read_shapefile(script_dir / "shp/phil/bounds/bounds.shp", cached=True)
# ph_gdf = ph_gdf.set_crs("epsg:4326")

land_mask = open_xr_dataset(script_dir / "python/input/nc/ph_mask.nc")

tz = pytz.timezone("Asia/Manila")
plot_proj = ccrs.PlateCarree()

xlim = (116, 128)
ylim = (5, 20)


def main(wrf_outs, out_dir):
    ds_proj = wrf_getproj(wrf_outs[0])
    init_dt = pd.to_datetime(
        wrf_getvar(wrf_outs[0], "T2", 0).time.values, utc=True
    ).astimezone(tz)

    for var_name, var_info in plot_vars_web.items():
        print(f"Plotting {var_name}...")

        timeidx = 24

        levels = var_info["levels"]
        colors = var_info["colors"]

        if var_name in ["wpd", "ppv"]:
            t0 = timeidx - 24
            _da = [wrf_getvar(wrf_outs, var_name, t) for t in range(t0, timeidx)]
            da_attrs = _da[0].attrs
            _da = xr.concat(_da, "time").sum("time")
            plt_types = ["mean", "max"]
        elif var_name == "temp":
            _da = wrf_getvar(wrf_outs, "T2", timeidx)
            da_attrs = _da.attrs
            _da = _da - 273.15
            plt_types = ["min", "max"]
        elif var_name == "wind":
            u = wrf_getvar(wrf_outs, "ua", timeidx, levels=850, interp="pressure")
            v = wrf_getvar(wrf_outs, "va", timeidx, levels=850, interp="pressure")
            _da = u.copy()
            _da.values = (u.values ** 2 + v.values ** 2) ** 0.5
            da_attrs = _da.attrs
            plt_types = ["min", "max"]
        elif var_name == "rainchance":
            _da = wrf_getvar(wrf_outs, "prcp", timeidx)
            _da = _da.where(_da <= 0.2, 1)
            _da = _da.where(_da > 0.2, 0)
            plt_types = ["sum"]
        else:
            continue

        for plt_type in plt_types:
            if plt_type == "max":
                da = _da.max("key_0")
            elif plt_type == "min":
                da = _da.min("key_0")
            elif plt_type == "sum":
                da = _da.sum("key_0")
            else:
                da = _da.mean("key_0")
            da.attrs = da_attrs
            da = da.salem.roi(roi=land_mask.z, crs=ds_proj)

            fig = plt.figure(figsize=(4, 5), constrained_layout=True)
            ax = plt.axes(projection=plot_proj)
            da.plot.contourf(
                ax=ax,
                transform=ds_proj,
                levels=levels,
                colors=colors,
                add_labels=False,
                add_colorbar=False,
                extend="both",
            )
            plt.axis("off")
            # ph_gdf.plot(ax=ax, facecolor="none")
            ax.set_extent((*xlim, *ylim))

            if var_name == "rainchance":
                out_file = (
                    out_dir / f"wrf-{var_name}_{init_dt.strftime('%Y-%m-%d_%H')}PHT.png"
                )
            else:
                out_file = (
                    out_dir
                    / f"wrf-{var_name}_{plt_type}_{init_dt.strftime('%Y-%m-%d_%H')}PHT.png"
                )
            fig.savefig(out_file, bbox_inches="tight", dpi=100, transparent=True)
            plt.close("all")


if __name__ == "__main__":
    wrf_out = ""
    out_dir = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile=", "odir="])
    except getopt.GetoptError:
        print("test.py -i <wrf_out file> -o <output dir>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("test.py -i <wrf_out file> -o <output dir>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            wrf_out = arg
        elif opt in ("-o", "--odir"):
            out_dir = Path(arg)
            out_dir.mkdir(parents=True, exist_ok=True)
    wrf_outs = [d / wrf_out for d in wrf_dirs]
    main(wrf_outs, out_dir)
