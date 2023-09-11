import sys
import getopt
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.colorbar import ColorbarBase

from const import plot_vars_web


def main(out_dir):
    for var_name, var_info in plot_vars_web.items():
        print(f"Plotting {var_name}...")

        if var_name == "rainchance":
            cbar_ext = "neither"
        else:
            cbar_ext = "both"

        fig = plt.figure(figsize=(8, 0.6))
        ax = plt.axes()

        cmap = ListedColormap(var_info["colors"])
        cmap.set_over("0.25")
        cmap.set_under("0.75")

        bounds = var_info["levels"]
        norm = BoundaryNorm(bounds, cmap.N, extend=cbar_ext)

        cb = ColorbarBase(
            ax,
            cmap=cmap,
            norm=norm,
            boundaries=bounds,
            extend=cbar_ext,
            extendfrac="auto",
            ticks=bounds,
            spacing="uniform",
            orientation="horizontal",
        )

        cb.ax.tick_params(labelcolor="white", labelsize=20)

        if var_name == "rainchance":
            cb.ax.get_xaxis().set_ticks([])
            for i, lab in enumerate(["LOW", "MED", "HIGH"]):
                cb.ax.text(
                    (2 * i + 1) / 2.0,
                    0.5,
                    lab,
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=20,
                )

        out_file = out_dir / f"wrf-{var_name}_cmap.png"
        fig.savefig(out_file, bbox_inches="tight", dpi=100, transparent=True)
        plt.close("all")


if __name__ == "__main__":
    out_dir = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:", ["odir="])
    except getopt.GetoptError:
        print("test.py -o <output dir>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("test.py -o <output dir>")
            sys.exit()
        elif opt in ("-o", "--odir"):
            out_dir = Path(arg)
            out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir)
