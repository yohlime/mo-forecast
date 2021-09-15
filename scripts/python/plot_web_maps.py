import pandas as pd
from salem import open_xr_dataset
from cartopy import crs as ccrs
import pytz

import matplotlib.pyplot as plt

from __const__ import plot_vars_web, script_dir

# ph_gdf = read_shapefile(script_dir / "shp/phil/bounds/bounds.shp", cached=True)
# ph_gdf = ph_gdf.set_crs("epsg:4326")

land_mask = open_xr_dataset(script_dir / "python/input/nc/ph_mask.nc")

tz = pytz.timezone("Asia/Manila")
plot_proj = ccrs.PlateCarree()

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
                plt_types = ["sum"]
            else:
                continue

            tt = (t + 1) * 24
            for plt_type in plt_types:
                if plt_type == "max":
                    da = _da.max("ens")
                elif plt_type == "min":
                    da = _da.min("ens")
                elif plt_type == "sum":
                    da = _da.sum("ens")
                else:
                    da = _da.mean("ens")
                da = da.salem.roi(roi=land_mask.z, crs=plot_proj)

                fig = plt.figure(figsize=(4, 5), constrained_layout=True)
                ax = plt.axes(projection=plot_proj)
                da.plot.contourf(
                    ax=ax,
                    transform=plot_proj,
                    levels=levels,
                    colors=colors,
                    add_labels=False,
                    add_colorbar=False,
                    extend="both",
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
