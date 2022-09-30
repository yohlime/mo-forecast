from datetime import timedelta
import numpy as np
import pandas as pd

from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

from __const__ import (
    tz,
    plot_proj,
    wrf_forecast_days,
    plot_vars,
    domain_land_mask as land_mask,
    trmm,
)

lon_formatter = LongitudeFormatter(zero_direction_label=True, degree_symbol="")
lat_formatter = LatitudeFormatter(degree_symbol="")

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
        plot_ens_mem = var_info.get("ens_mem", False)
        for t in range(wrf_forecast_days):
            print(f"Day {t+1}...")

            if var_name in ["rain", "rh", "wpd", "ppv"]:
                das = {"ens": ds[var_name].isel(time=t).mean("ens")}
                if plot_ens_mem:
                    for ens_idx in ds[var_name].ens.values:
                        das[f"run{int(ens_idx)+1}"] = ds[var_name].isel(
                            time=t, ens=ens_idx
                        )
            elif var_name == "rainx":
                das = {"ens": ds["rain"].isel(time=t).mean("ens")}
            elif var_name == "temp":
                _da = (
                    ds["tsk"]
                    .isel(time=t)
                    .mean("ens")
                    .salem.roi(roi=land_mask.mask.isnull())
                )
                _das = {"ens": _da}
                da = ds[var_name].isel(time=t).mean("ens").salem.roi(roi=land_mask.mask)
                da.values = _da.fillna(0).values + da.fillna(0).values
                das = {"ens": da}
            elif var_name in ["hi", "hix"]:
                _da = ds[var_name].isel(time=t).mean("ens")
                das = {"ens": _da.salem.roi(roi=land_mask.mask, crs=plot_proj)}
            elif var_name == "wind":
                _u = ds["u_850hPa"].isel(time=t).mean("ens")
                _v = ds["v_850hPa"].isel(time=t).mean("ens")
                u = _u[::20, ::20]
                v = _v[::20, ::20]
                da = u.copy()
                da.values = (u.values**2 + v.values**2) ** 0.5
                das = {"ens": da}
            else:
                continue

            for da_name, da in das.items():
                dt1 = pd.to_datetime(da.time.values, utc=True).astimezone(tz)
                dt1_str = dt1.strftime("%Y-%m-%d %H")
                dt2 = dt1 + timedelta(days=1)
                dt2_str = dt2.strftime("%Y-%m-%d %H")
                plt_title = (
                    f"{var_info['title']}\nValid from {dt1_str} to {dt2_str} PHT"
                )
                plt_annotation = (
                    f"WRF ensemble forecast initialized at {init_dt_str} PHT."
                )

                fig = plt.figure(figsize=(8, 9), constrained_layout=True)
                ax = plt.axes(projection=plot_proj)
                ax.xaxis.set_major_formatter(lon_formatter)
                ax.yaxis.set_major_formatter(lat_formatter)
                ax.set_xticks(lon_labels, crs=plot_proj)
                ax.set_yticks(lat_labels, crs=plot_proj)

                if var_name == "rainx":
                    trmm2 = trmm.isel(time=da.time.dt.month.values - 1)
                    trmm2.name = da.name
                    trmm2 = trmm2.assign_coords(
                        time=da.time,
                    )
                    extreme_da = np.divide(da, trmm2) * 100
                elif var_name == "temp":
                    p = _das[da_name].plot.contour(
                        ax=ax,
                        transform=plot_proj,
                        levels=range(28, 32),
                        colors="#ffffff",
                        add_labels=False,
                        linewidths=0.5,
                    )
                    ax.clabel(p, p.levels, inline=True, fontsize=6)
                elif var_name == "wind":
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
                elif var_name == "ppv":
                    da = da.salem.roi(roi=land_mask.mask)

                fig.suptitle(plt_title, fontsize=14)

                if var_name in ["wpd", "ppv"]:
                    text_color = "blue"
                    if var_name == "ppv":
                        text_color = "darkorange"

                    tot_wpd = da.salem.roi(roi=land_mask.mask).sum().values / 1000
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
                if var_name == "rainx":
                    da.where(extreme_da < 100).plot.contourf(
                        ax=ax,
                        transform=plot_proj,
                        levels=levels,
                        colors="white",
                        alpha=1,
                        extend="both",
                        add_labels=False,
                        add_colorbar=False,
                    )
                p.colorbar.ax.set_title(f"[{var_info['units']}]", pad=20, fontsize=10)
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
                file_prfx = "wrf"
                if "run" in da_name:
                    file_prfx += f"_{da_name}"
                out_file = (
                    out_dir
                    / f"{file_prfx}-{tt}hr_{var_name}_{init_dt.strftime('%Y-%m-%d_%H')}PHT.png"
                )
                fig.savefig(out_file, bbox_inches="tight", dpi=300)
                plt.close("all")
