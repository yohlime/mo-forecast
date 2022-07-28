# Description: Plot n-day total gsmap precipitation for extreme weather bulletin
# Author: Kevin Henson
# Last edited: July 28, 2022

import matplotlib.pyplot as plt
import datetime as dt
import cartopy.crs as ccrs
import numpy as np
from pathlib import Path
import os
import salem
from __const__ import cmap_ewb, norm_ewb


gsmap_dir = Path(os.getenv("GSMAP_NC_DIR"))
outdir = Path("/home/modelman/forecast/output/web/maps/ewb/")


def plot_total_rain():

    # Loop through past n days
    for day in np.arange(1, max(days_list) + 1):

        # Set date variable
        dt_var = today - dt.timedelta(int(day))

        # Access gsmap file and data
        gsmap_fn = gsmap_dir / f"gsmap_gauge_{dt_var}_00_day.nc"
        if gsmap_fn.is_file():
            if day == 1:
                gsmap_ds = salem.open_xr_dataset(gsmap_fn)
            else:
                gsmap_ds += salem.open_xr_dataset(gsmap_fn)

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

            ax.set_title(
                f"{day}-day GSMaP Total Precipitation (mm) \n{dt_var}_08 PHT to "
                f"{str(today)}_08 PHT"
            )

            out_file = outdir / f"gsmap_{day}day_totalprecip_latest.png"

            print(f"Saving ewb {out_file}...")

            fig.savefig(out_file, bbox_inches="tight", dpi=300)
            plt.close("all")


if __name__ == "__main__":
    today = dt.date.today()
    # today = dt.date(2022, 6, 5) # for testing

    outdir.mkdir(parents=True, exist_ok=True)

    # aws columns
    aws_cols = ["name", "timestamp", "rr", "lat", "lon"]

    # set day range
    days_list = [1, 3, 5, 7, 30]
    plot_total_rain()
