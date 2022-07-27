# Description: Plot n-day total precipitation for extreme weather bulletin
# Author: Kevin Henson
# Last edited: July 27, 2022

import matplotlib.pyplot as plt
import datetime as dt
import cartopy.crs as ccrs
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.colors as mcolors

# import cartopy.io.img_tiles as cimgt
import cartopy.io.shapereader as shpreader
from cartopy.feature import ShapelyFeature

# import cartopy.feature as cfeature
# import sys


def plot_total_rain(days, outdir):

    # Intialize dataframe
    df_aws = pd.DataFrame(columns=aws_cols)

    # Loop through past n days
    for day in np.arange(1, days + 1):

        # Set date variable
        dt_var = today - dt.timedelta(int(day))
        dt_var_str = str(dt_var)

        # Read station data
        aws_fn = Path(aws_dir + "stn_obs_24hr_" + dt_var_str + "_08PHT.csv")
        if aws_fn.exists():

            aws_df = pd.read_csv(aws_fn, usecols=aws_cols, na_values="-999.000000")
            df_aws = pd.concat([df_aws, aws_df])

    # Get 7 day total precip
    df_sum = df_aws.groupby(["name"])["rr"].sum()
    df_lat_lon = df_aws.groupby(["name"])[["lat", "lon"]].first()
    df_sum = pd.concat([df_sum, df_lat_lon], axis=1)

    # Plot
    # request = cimgt.GoogleTiles()
    # fig, ax = plt.subplots(subplot_kw=dict(projection=request.crs))
    fig, ax = plt.subplots(subplot_kw=dict(projection=ccrs.PlateCarree()))
    extents = [120.76, 121.33, 14.24, 14.87]
    ax.set_extent(extents)
    # ax.add_image(request, 10)

    # Display shape files
    for muni in mm:
        shape_feature = ShapelyFeature(
            [muni.geometry],
            ccrs.PlateCarree(),
            facecolor="white",
            zorder=1,
            edgecolor="black",
            lw=0.1,
        )
        ax.add_feature(shape_feature)

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

    lon = df_sum["lon"]
    lat = df_sum["lat"]
    pr = df_sum["rr"]

    # Plot station data
    cs = ax.scatter(
        lon,
        lat,
        s=20,
        c=pr,
        edgecolor="black",
        linewidth=0.3,
        alpha=1,
        transform=ccrs.PlateCarree(),
        cmap=cmap,
        norm=norm,
    )

    cbar_ax = fig.add_axes([0.26, 0.04, 0.5, 0.02])
    fig.colorbar(cs, cax=cbar_ax, orientation="horizontal", extend="max")

    ax.set_title(
        f"{days}-day Total Precipitation (mm) \n{dt_var_str}_08 PHT to "
        "{str(today)}_08 PHT"
    )

    out_file = outdir / f"station_{days}day_totalprecip_latest.png"

    print(f"Saving ewb {out_file}...")

    fig.savefig(out_file, bbox_inches="tight", dpi=300)
    plt.close("all")


if __name__ == "__main__":
    today = dt.date.today()
    # today = dt.date(2022, 6, 5) # for testing

    aws_dir = "/home/modelman/forecast/input/aws_files/"
    shp_dir = "resources/ph_adm_shp/"
    outdir = Path("/home/modelman/forecast/output/web/maps/ewb/")

    outdir.mkdir(parents=True, exist_ok=True)

    # Read shape file
    reader = shpreader.Reader(f"{shp_dir}PHL_adm2.shp")
    provinces = ["Metropolitan Manila", "Rizal", "Bulacan", "Cavite", "Laguna"]
    mm = [muni for muni in reader.records() if muni.attributes["NAME_1"] in provinces]

    # color map
    clevs = [0, 10, 20, 60, 100, 200, 300, 400, 500, 600, 700, 1000]
    cmap_data = [
        (1.0, 1.0, 1.0),
        (0.3137255012989044, 0.8156862854957581, 0.8156862854957581),
        (0.0, 1.0, 1.0),
        (0.0, 0.8784313797950745, 0.501960813999176),
        (0.0, 0.7529411911964417, 0.0),
        (0.501960813999176, 0.8784313797950745, 0.0),
        (1.0, 1.0, 0.0),
        (1.0, 0.6274510025978088, 0.0),
        (1.0, 0.0, 0.0),
        (1.0, 0.125490203499794, 0.501960813999176),
        (0.9411764740943909, 0.250980406999588, 1.0),
        (0.501960813999176, 0.125490203499794, 1.0),
    ]

    cmap = mcolors.ListedColormap(cmap_data, "precipitation")
    norm = mcolors.BoundaryNorm(clevs, cmap.N)

    # aws columns
    aws_cols = ["name", "timestamp", "rr", "lat", "lon"]

    day_range = [1, 3, 5, 7, 30]
    for dr in day_range:
        plot_total_rain(dr, outdir)
