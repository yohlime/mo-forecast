from datetime import timedelta
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from __const__ import tz

# SACASOL
station_name = "SACASOL"
site_lon = 123.434974
site_lat = 10.516037
# SOLARACE1
station_name2 = "SOLARACE1"
site_lon2 = 121.22
site_lat2 = 14.07

def plot_ts_ace(ds, out_dir):
    init_dt = pd.to_datetime(ds.time.values[0], utc=True).astimezone(tz)

    site_df = ds.sel(lon=site_lon, lat=site_lat, method="nearest").to_dataframe()
    site_df = site_df.groupby("time").mean()
    site_df.index = site_df.index.tz_localize("utc").tz_convert(tz)

    site_df2 = ds.sel(lon=site_lon2, lat=site_lat2, method="nearest").to_dataframe()
    site_df2 = site_df2.groupby("time").mean()
    site_df2.index = site_df2.index.tz_localize("utc").tz_convert(tz)

    t_range = pd.date_range(init_dt, periods=121, freq="H")
    x_range = range(0, site_df.shape[0])

    x_major_step = 24
    x_minor_step = 6
    t_major_ticks = t_range[t_range.hour == 0]
    t_minor_ticks = t_range[(t_range.hour % x_minor_step) == 0]
    x_major_ticks = [t_range.get_loc(t) for t in t_major_ticks]
    x_minor_ticks = [t_range.get_loc(t) for t in t_minor_ticks]

    fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(25, 11), constrained_layout=True)

    ############### GHI forecast ##################

    # region plot GHI SACASOL
    site_df.plot.bar(
        y="ghi",
        edgecolor="red",
        facecolor="red",
        ax=axs[0],
        label="SACASOL",
    )
    _ax = axs[0].twiny()
    _t_major_ticks = t_major_ticks - timedelta(hours=12)
    _ax.set_xticks([x - 12 for x in x_major_ticks])
    _ax.set_xticklabels(_t_major_ticks.strftime("%A %b %-d"))
    _ax.tick_params(axis="x", labelsize=22, top=False)
    _ax.set_xlabel(None)
    _ax.set_xlim([-2, 121])
    axs[0].set_xticks(x_major_ticks)
    axs[0].set_xticklabels(t_major_ticks.strftime("%a %H:00"))
    axs[0].set_xticks(x_minor_ticks, minor=True)
    axs[0].set_xticklabels(
        t_minor_ticks.strftime("%a %H:00"),
        minor=True,
    )
    axs[0].tick_params(axis="x", which="both", labelsize=22, labelrotation=30)
    axs[0].set_xlabel("Day and Time (PHT)", fontsize=24)
    axs[0].set_xlim([-2, 121])

    axs[0].set_yticks(np.linspace(0, 1500, 5))
    axs[0].tick_params(axis="y", labelsize=24)
    axs[0].set_ylabel("GHI (W m-2)", fontsize=24, color="black")
    axs[0].set_ylim([0, 1500])

    axs[0].grid(which="major", c="gray", ls="dotted")

    axs[0].legend(loc="upper right", fontsize=24)
    axs[0].set_title(
        f"Global Horizontal Irradiance Ensemble Forecast ({station_name})\nInitialized at {init_dt.strftime('%Y-%m-%d %H')}:00 PHT",
        pad=38,
        fontsize=30,
    )
    # endregion plot GHI SACASOL

    # region plot GHI SOLARACE1
    site_df2.plot.bar(
        y="ghi",
        edgecolor="goldenrod",
        facecolor="goldenrod",
        ax=axs[1],
        label="SOLARACE1",
    )
    _ax = axs[1].twiny()
    _t_major_ticks = t_major_ticks - timedelta(hours=12)
    _ax.set_xticks([x - 12 for x in x_major_ticks])
    _ax.set_xticklabels(_t_major_ticks.strftime("%A %b %-d"))
    _ax.tick_params(axis="x", labelsize=22, top=False)
    _ax.set_xlabel(None)
    _ax.set_xlim([-2, 121])
    axs[1].set_xticks(x_major_ticks)
    axs[1].set_xticklabels(t_major_ticks.strftime("%a %H:00"))
    axs[1].set_xticks(x_minor_ticks, minor=True)
    axs[1].set_xticklabels(
        t_minor_ticks.strftime("%a %H:00"),
        minor=True,
    )
    axs[1].tick_params(axis="x", which="both", labelsize=22, labelrotation=30)
    axs[1].set_xlabel("Day and Time (PHT)", fontsize=24)
    axs[1].set_xlim([-2, 121])

    axs[1].set_yticks(np.linspace(0, 1500, 5))
    axs[1].tick_params(axis="y", labelsize=24)
    axs[1].set_ylabel("GHI (W m-2)", fontsize=24, color="black")
    axs[1].set_ylim([0, 1500])

    axs[1].grid(which="major", c="gray", ls="dotted")

    axs[1].legend(loc="upper right", fontsize=24)
    axs[1].set_title(
        f"Global Horizontal Irradiance Ensemble Forecast ({station_name2})\nInitialized at {init_dt.strftime('%Y-%m-%d %H')}:00 PHT",
        pad=38,
        fontsize=30,
    )
    # endregion plot GHI SOLARACE1
    ############### solar energy forecast ##################
    
    # # region plot PPV SACASOL
    # site_df.plot.bar(
    #     y="ppv",
    #     edgecolor="red",
    #     facecolor="red",
    #     ax=axs[0],
    #     label="SACASOL",
    # )
    # _ax = axs[0].twiny()
    # _t_major_ticks = t_major_ticks - timedelta(hours=12)
    # _ax.set_xticks([x - 12 for x in x_major_ticks])
    # _ax.set_xticklabels(_t_major_ticks.strftime("%A %b %-d"))
    # _ax.tick_params(axis="x", labelsize=22, top=False)
    # _ax.set_xlabel(None)
    # _ax.set_xlim([-2, 121])
    # axs[0].set_xticks(x_major_ticks)
    # axs[0].set_xticklabels(t_major_ticks.strftime("%a %H:00"))
    # axs[0].set_xticks(x_minor_ticks, minor=True)
    # axs[0].set_xticklabels(
    #     t_minor_ticks.strftime("%a %H:00"),
    #     minor=True,
    # )
    # axs[0].tick_params(axis="x", which="both", labelsize=22, labelrotation=30)
    # axs[0].set_xlabel("Day and Time (PHT)", fontsize=24)
    # axs[0].set_xlim([-2, 121])

    # axs[0].set_yticks(np.linspace(0, 2, 5))
    # axs[0].tick_params(axis="y", labelsize=24)
    # axs[0].set_ylabel("Solar PP (MW)", fontsize=24, color="black")
    # axs[0].set_ylim([0, 2])

    # axs[0].grid(which="major", c="gray", ls="dotted")

    # axs[0].legend(loc="upper right", fontsize=24)
    # axs[0].set_title(
    #     f"Solar Power Ensemble Forecast ({station_name})\nInitialized at {init_dt.strftime('%Y-%m-%d %H')}:00 PHT",
    #     pad=38,
    #     fontsize=30,
    # )
    # # endregion plot PPV SACASOL

    # # region plot PPV SOLARACE1
    # site_df2.plot.bar(
    #     y="ppv",
    #     edgecolor="goldenrod",
    #     facecolor="goldenrod",
    #     ax=axs[1],
    #     label="SOLARACE1",
    # )

    # axs[1].set_xticks(x_major_ticks)
    # axs[1].set_xticklabels(t_major_ticks.strftime("%a %H:00"))
    # axs[1].set_xticks(x_minor_ticks, minor=True)
    # axs[1].set_xticklabels(
    #     t_minor_ticks.strftime("%a %H:00"),
    #     minor=True,
    # )
    # axs[1].tick_params(axis="x", which="both", labelsize=22, labelrotation=30)
    # axs[1].set_xlabel("Day and Time (PHT)", fontsize=24)
    # axs[1].set_xlim([-2, 121])

    # axs[1].set_yticks(np.linspace(0, 2, 5))
    # axs[1].tick_params(axis="y", labelsize=24)
    # axs[1].set_ylabel("Solar PP (MW)", fontsize=24, color="black")
    # axs[1].set_ylim([0, 2])

    # axs[1].grid(which="major", c="gray", ls="dotted")

    # axs[1].legend(loc="upper right", fontsize=24)
    # axs[1].set_title(
    #     f"Solar Power Ensemble Forecast ({station_name2})\nInitialized at {init_dt.strftime('%Y-%m-%d %H')}:00 PHT",
    #     pad=38,
    #     fontsize=30,
    # )
    # # endregion plot PPV SOLARACE1

    out_file = out_dir / f"acenergy-ts_{init_dt.strftime('%Y-%m-%d_%H')}PHT.png"
    fig.savefig(out_file, bbox_inches="tight", dpi=300)
    plt.close("all")
