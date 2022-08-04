# Description: Plot n-day total gsmap precipitation for extreme weather bulletin
# Author: Kevin Henson
# Last edited: Aug. 3, 2022

import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import cartopy.crs as ccrs
import numpy as np
from pathlib import Path
import os
import salem
from __const__ import cmap_ewb, norm_ewb


gsmap_dir = Path(os.getenv("GSMAP_NC_DIR"))
outdir = Path("/home/modelman/forecast/output/web/maps/ewb/")

yy = int(os.getenv("FCST_YY_GSMAP"))
mm = int(os.getenv("FCST_MM_GSMAP"))
dd = int(os.getenv("FCST_DD_GSMAP"))
# zz = int(os.getenv("FCST_ZZ_GSMAP"))
zz = 0  # 8am values

# set start date
sd = datetime(yy, mm, dd, zz)

# set end date for label PHT
ed = sd + timedelta(hours=32)
ed_label = ed.strftime("%Y-%m-%d_%H")

# create output directory
outdir.mkdir(parents=True, exist_ok=True)

# set day range
days_list = [1, 3, 5, 7, 30]


def plot_total_rain():

    # Loop through past n days
    for day in np.arange(0, max(days_list)):

        # Set date variable
        dt_var = sd - timedelta(int(day))
        dt_var_str = dt_var.strftime("%Y-%m-%d_%H")

        # Access gsmap file and data
        gsmap_fn = gsmap_dir / f"gsmap_gauge_{dt_var_str}_day.nc"
        if gsmap_fn.is_file():
            if day == 0:
                gsmap_ds = salem.open_xr_dataset(gsmap_fn)
            else:
                gsmap_ds += salem.open_xr_dataset(gsmap_fn)
        else:
            print(f"No file: {gsmap_fn}")

        day += 1
        if day in days_list:
            # Plot
            fig, ax = plt.subplots(subplot_kw=dict(projection=ccrs.PlateCarree()))
            extents = [115.0, 128.9, 4.85, 20.95]
            ax.set_extent(extents)

            ax.coastlines(linewidth=0.5)

            gl = ax.gridlines(
                crs=ccrs.PlateCarree(),
                draw_labels=True,
                linewidth=1,
                color="gray",
                alpha=0,
                linestyle="--",
            )
            gl.top_labels = False
            gl.right_labels = False
            gl.xlabel_style = {"size": 7}
            gl.ylabel_style = {"size": 7}

            lon = gsmap_ds.lon
            lat = gsmap_ds.lat
            pr = gsmap_ds.precip

            # Plot station data
            cs = ax.pcolor(
                lon,
                lat,
                pr,
                transform=ccrs.PlateCarree(),
                cmap=cmap_ewb,
                norm=norm_ewb,
            )

            cbar_ax = fig.add_axes([0.26, 0.04, 0.5, 0.02])
            fig.colorbar(cs, cax=cbar_ax, orientation="horizontal", extend="max")

            # Set date variable PHT
            dt_var_moving = dt_var + timedelta(hours=8)
            dt_var_str = dt_var_moving.strftime("%Y-%m-%d_%H")

            ax.set_title(
                f"{day}-day GSMaP Total Precipitation (mm) \n{dt_var_str} PHT to "
                f"{ed_label} PHT"
            )

            out_file = outdir / f"gsmap_{day}day_totalprecip_latest.png"

            print(f"Saving ewb {out_file}...")

            fig.savefig(out_file, bbox_inches="tight", dpi=300)
            plt.close("all")


if __name__ == "__main__":
    plot_total_rain()
