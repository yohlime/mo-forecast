import pandas as pd

import matplotlib.pyplot as plt

from __const__ import tz, plot_proj, plot_vars_web, ph_land_mask as land_mask

xlim = (116, 128)
ylim = (5, 20)


def plot_web_maps(ds, out_dir):
    init_dt = pd.to_datetime(ds.time.values[0], utc=True).astimezone(tz)

    for var_name, var_info in plot_vars_web.items():
        print(f"Plotting {var_name}...")
        levels = var_info["levels"]
        colors = var_info["colors"]
        for t in range(2):
            print(f"Day {t+1}...")

            if var_name in ["wpd", "ppv"]:
                _da = ds[var_name].isel(time=t)
                plt_types = ["mean", "max"]
            elif var_name == "temp":
                _da = ds[var_name].isel(time=t)
                plt_types = ["min", "max"]
            elif var_name == "wind":
                u = ds["u_850hPa"].isel(time=t)
                v = ds["v_850hPa"].isel(time=t)
                _da = u.copy()
                _da.values = (u.values ** 2 + v.values ** 2) ** 0.5
                plt_types = ["min", "max"]
            elif var_name == "rainchance":
                _da = ds["rain"].isel(time=t)
                no_rain = _da <= 0.2
                _da = _da.where(no_rain, 1)
                _da = _da.where(~no_rain, 0)
                plt_types = ["mean"]
            else:
                continue

            cbar_extend = "both"
            if var_name == "rainchance":
                cbar_extend = "min"

            tt = (t + 1) * 24
            for plt_type in plt_types:
                if plt_type == "max":
                    da = _da.max("ens")
                    if var_name == "wind":
                        _u = u.max("ens")
                        _v = v.max("ens")
                elif plt_type == "min":
                    da = _da.min("ens")
                    if var_name == "wind":
                        _u = u.min("ens")
                        _v = v.min("ens")
                elif plt_type == "sum":
                    da = _da.sum("ens")
                else:
                    da = _da.mean("ens")
                da = da.salem.roi(roi=land_mask.mask, crs=plot_proj)

                fig = plt.figure(figsize=(4, 5), constrained_layout=True)
                ax = plt.axes(projection=plot_proj)
                
                da.plot.contourf(
                    ax=ax,
                    transform=plot_proj,
                    levels=levels,
                    colors=colors,
                    add_labels=False,
                    add_colorbar=False,
                    extend=cbar_extend,
                )

                if var_name == "wind":
                    
                    plt.streamplot(
                        _u.lon.values,
                        _u.lat.values,
                        _u.values,
                        _v.values,
                        density=2,
                        color="white",
                        linewidth=0.5,
                        transform=plot_proj,
                    ) 

                plt.axis("off")
                # ph_gdf.plot(ax=ax, facecolor="none")
                ax.set_extent((*xlim, *ylim))

                out_file = f"wrf-{tt}hr_{var_name}_{plt_type}_{init_dt.strftime('%Y-%m-%d_%H')}PHT.png"
                if var_name == "rainchance":
                    out_file = f"wrf-{tt}hr_{var_name}_{init_dt.strftime('%Y-%m-%d_%H')}PHT.png"
                out_file = out_dir / out_file
                fig.savefig(out_file, bbox_inches="tight", dpi=100, transparent=True)
                plt.close("all")
