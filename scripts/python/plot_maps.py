import pandas as pd
from salem import open_xr_dataset
from cartopy import crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from datetime import timedelta
import pytz

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

from __const__ import wrf_forecast_days, plot_vars, script_dir

land_mask = open_xr_dataset(script_dir / "python/input/nc/mask.nc")

tz = pytz.timezone("Asia/Manila")

lon_formatter = LongitudeFormatter(zero_direction_label=True, degree_symbol="")
lat_formatter = LatitudeFormatter(degree_symbol="")
plot_proj = ccrs.PlateCarree()

lon_labels = range(120, 130, 5)
lat_labels = range(5, 25, 5)
xlim = (116, 128)
ylim = (5, 20)


def plot_maps(ds, out_dir):
    init_dt = pd.to_datetime(ds.time.values[0], utc=True).astimezone(tz)
    init_dt_str = init_dt.strftime("%Y-%m-%d %H")

    for var_name, var_info in plot_vars.items():
        print(f"Plotting {var_name}...")
        levels = var_info["levels"]
        colors = var_info["colors"]
        for t in range(wrf_forecast_days):
            print(f"Day {t+1}...")

            fig = plt.figure(figsize=(8, 9), constrained_layout=True)
            ax = plt.axes(projection=plot_proj)
            ax.xaxis.set_major_formatter(lon_formatter)
            ax.yaxis.set_major_formatter(lat_formatter)
            ax.set_xticks(lon_labels, crs=plot_proj)
            ax.set_yticks(lat_labels, crs=plot_proj)

            if var_name == "rain":
                da = ds[var_name].isel(time=t).mean("ens")
            elif var_name == "temp":
                da = ds["tsk"].isel(time=t).mean("ens")
                da = da.salem.roi(roi=land_mask.z.isnull())
                p = da.plot.contour(
                    ax=ax,
                    transform=plot_proj,
                    levels=range(28, 32),
                    colors="#ffffff",
                    add_labels=False,
                    linewidths=0.5,
                )
                ax.clabel(p, p.levels, inline=True, fontsize=6)
                _da = ds[var_name].isel(time=t).mean("ens")
                _da = _da.salem.roi(roi=land_mask.z)
                da.values = da.fillna(0).values + _da.fillna(0).values
            elif var_name == "hi":
                da = ds[var_name].isel(time=t).mean("ens")
                da = da.salem.roi(roi=land_mask.z, crs=plot_proj)
            elif var_name == "rh":
                da = ds[var_name].isel(time=t).mean("ens")
            elif var_name == "wind":
                _u = ds["u_850hPa"].isel(time=t).mean("ens")
                _v = ds["v_850hPa"].isel(time=t).mean("ens")
                u = _u[::20, ::20]
                v = _v[::20, ::20]
                da = u.copy()
                da.values = (u.values ** 2 + v.values ** 2) ** 0.5
                cmap = ListedColormap(colors)
                norm = BoundaryNorm(levels, cmap.N, extend="both")
                p = plt.barbs(
                    u.lon.values,
                    u.lat.values,
                    u.values,
                    v.values,
                    da.values,
                    length=6,
                    cmap=cmap,
                    norm=norm,
                    transform=plot_proj,
                )
                plt.colorbar(p, ticks=levels, shrink=0.5)
            elif var_name in ["wpd", "ppv"]:
                da = ds[var_name].isel(time=t).mean("ens")
                if var_name == "wpd":
                    text_color = "blue"
                elif var_name == "ppv":
                    da = da.salem.roi(roi=land_mask.z)
                    text_color = "darkorange"
            else:
                continue

            dt1 = pd.to_datetime(da.time.values, utc=True).astimezone(tz)
            dt1_str = dt1.strftime("%Y-%m-%d %H")
            dt2 = dt1 + timedelta(days=1)
            dt2_str = dt2.strftime("%Y-%m-%d %H")
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
                    transform=plot_proj,
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

            tt = (t + 1) * 24
            out_file = (
                out_dir
                / f"wrf-{tt}hr_{var_name}_{init_dt.strftime('%Y-%m-%d_%H')}PHT.png"
            )
            fig.savefig(out_file, bbox_inches="tight", dpi=300)
            plt.close("all")
