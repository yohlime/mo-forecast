import sys
import getopt
from pathlib import Path
import pandas as pd
import xarray as xr
from salem import open_xr_dataset
from cartopy import crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from datetime import timedelta
import pytz

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

from wrf import omp_set_num_threads, omp_get_max_threads

from __const__ import wrf_dirs, plot_vars, wrf_forecast_days, script_dir
from __helper__ import wrf_getvar, wrf_getproj


omp_set_num_threads(omp_get_max_threads())
print(f"Using {omp_get_max_threads()} threads...")

land_mask = open_xr_dataset(script_dir / "python/input/nc/mask.nc")

tz = pytz.timezone("Asia/Manila")

lon_formatter = LongitudeFormatter(zero_direction_label=True, degree_symbol="")
lat_formatter = LatitudeFormatter(degree_symbol="")
plot_proj = ccrs.PlateCarree()

lon_labels = range(120, 130, 5)
lat_labels = range(5, 25, 5)
xlim = (116, 128)
ylim = (5, 20)


def main(wrf_outs, out_dir):
    ds_proj = wrf_getproj(wrf_outs[0])
    init_dt = pd.to_datetime(
        wrf_getvar(wrf_outs[0], "T2", 0).time.values, utc=True
    ).astimezone(tz)
    init_dt_str = init_dt.strftime("%Y-%m-%d %H")

    for var_name, var_info in plot_vars.items():
        print(f"Plotting {var_name}...")
        for day in range(1, wrf_forecast_days + 1):
            print(f"Day {day}...")
            timeidx = day * 24

            levels = var_info["levels"]
            colors = var_info["colors"]

            fig = plt.figure(figsize=(8, 9), constrained_layout=True)
            ax = plt.axes(projection=plot_proj)
            ax.xaxis.set_major_formatter(lon_formatter)
            ax.yaxis.set_major_formatter(lat_formatter)
            ax.set_xticks(lon_labels, crs=plot_proj)
            ax.set_yticks(lat_labels, crs=plot_proj)

            if var_name == "rain":
                da = wrf_getvar(wrf_outs, "prcp", timeidx)
                if day > 1:
                    _timeidx = timeidx - 24
                    da.values = (
                        da.values - wrf_getvar(wrf_outs, "prcp", _timeidx).values
                    )
                da_attrs = da.attrs
                da = da.mean("key_0")
                da.attrs = da_attrs
            elif var_name == "temp":
                da = wrf_getvar(wrf_outs, "TSK", timeidx)
                da_attrs = da.attrs
                da = da.mean("key_0")
                da = da - 273.15
                da.attrs = da_attrs
                da = da.salem.roi(roi=land_mask.z.isnull())
                p = da.plot.contour(
                    ax=ax,
                    transform=ds_proj,
                    levels=range(28, 32),
                    colors="#ffffff",
                    linewidths=0.5,
                )
                ax.clabel(p, p.levels, inline=True, fontsize=6)
                _da = wrf_getvar(wrf_outs, "T2", timeidx)
                da_attrs = _da.attrs
                _da = _da.mean("key_0")
                _da = _da - 273.15
                _da.attrs = da_attrs
                _da = _da.salem.roi(roi=land_mask.z)
                da.values = da.fillna(0).values + _da.fillna(0).values
            elif var_name == "hi":
                da = wrf_getvar(wrf_outs, "hi", timeidx)
                da_attrs = da.attrs
                da = da.mean("key_0")
                da.attrs = da_attrs
                da = da.salem.roi(roi=land_mask.z, crs=ds_proj)
            elif var_name == "rh":
                da = wrf_getvar(wrf_outs, "rh2", timeidx)
                da_attrs = da.attrs
                da = da.mean("key_0")
                da.attrs = da_attrs
            elif var_name == "wind":
                _u = wrf_getvar(wrf_outs, "ua", timeidx, levels=850, interp="pressure")
                _u = _u.mean("key_0")
                _v = wrf_getvar(wrf_outs, "va", timeidx, levels=850, interp="pressure")
                _v = _v.mean("key_0")
                u = _u[::20, ::20]
                v = _v[::20, ::20]
                wspd = (u.values ** 2 + v.values ** 2) ** 0.5
                cmap = ListedColormap(colors)
                norm = BoundaryNorm(levels, cmap.N, extend="both")
                p = plt.barbs(
                    u.lon.values,
                    u.lat.values,
                    u.values,
                    v.values,
                    wspd,
                    length=6,
                    cmap=cmap,
                    norm=norm,
                    transform=plot_proj,
                )
                plt.colorbar(p, ticks=levels, shrink=0.5)
            elif var_name in ["wpd", "ppv"]:
                t0 = timeidx - 24
                da = [wrf_getvar(wrf_outs, var_name, t) for t in range(t0, timeidx)]
                da_attrs = da[0].attrs
                ts = pd.to_datetime(da[-1].time.values) + timedelta(hours=1)
                da = xr.concat(da, "time").sum("time")
                da = da.mean("key_0")
                da.attrs = da_attrs
                da = da.assign_coords({"time": ts})
                if var_name == "wpd":
                    text_color = "blue"
                elif var_name == "ppv":
                    da = da.salem.roi(roi=land_mask.z)
                    text_color = "darkorange"
            else:
                continue

            dt2 = pd.to_datetime(da.time.values, utc=True).astimezone(tz)
            dt2_str = dt2.strftime("%Y-%m-%d %H")
            dt1 = dt2 - timedelta(days=1)
            dt1_str = dt1.strftime("%Y-%m-%d %H")
            plt_title = f"{var_info['title']}\nValid from {dt1_str} to {dt2_str} PHT"
            plt_annotation = f"WRF ensemble forecast initialized at {init_dt_str} PHT."

            fig.suptitle(plt_title, fontsize=14)

            if var_name in ["wpd", "ppv"]:
                tot_wpd = da.salem.roi(roi=land_mask.z).sum().values / 1000
                tot_wpd = int(tot_wpd.round())
                ax.set_title(
                    f"Total$^{{*}}$: {tot_wpd} GW", fontsize=24, color=text_color
                )

            if var_name != "wind":
                p = da.plot.contourf(
                    ax=ax,
                    transform=ds_proj,
                    levels=levels,
                    colors=colors,
                    add_labels=False,
                    extend="both",
                    cbar_kwargs=dict(shrink=0.5),
                )
            p.colorbar.ax.set_title(f"[{var_info['units']}]", fontsize=10)
            ax.coastlines()
            ax.set_extent((*xlim, *ylim))
            if var_name in ["wpd", "ppv"]:
                ax.annotate(
                    "$^{*}$Philippine landmass only",
                    xy=(5, -30),
                    xycoords="axes points",
                    fontsize=8,
                    color=text_color,
                )
                ax.annotate(
                    plt_annotation, xy=(5, -40), xycoords="axes points", fontsize=8
                )
            else:
                ax.annotate(
                    plt_annotation, xy=(5, -30), xycoords="axes points", fontsize=8
                )
            ax.annotate(
                "observatory.ph",
                xy=(10, 10),
                xycoords="axes points",
                fontsize=10,
                bbox=dict(boxstyle="square,pad=0.3", alpha=0.5),
                alpha=0.5,
            )

            out_file = (
                out_dir
                / f"wrf-{timeidx}hr_{var_name}_{init_dt.strftime('%Y-%m-%d_%H')}PHT.png"
            )
            fig.savefig(out_file, bbox_inches="tight", dpi=300)
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
