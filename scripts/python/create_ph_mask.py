import sys
import getopt
from pathlib import Path
from salem import open_xr_dataset, read_shapefile

from __const__ import script_dir


def main(out_file):
    ph_gdf = read_shapefile(script_dir / "shp/phil/bounds/bounds.shp", cached=True)
    ph_gdf = ph_gdf.set_crs("epsg:4326")

    land_mask = open_xr_dataset(script_dir / "python/input/nc/mask.nc")
    land_mask = land_mask.salem.roi(shape=ph_gdf)
    land_mask.to_netcd(out_file)


if __name__ == "__main__":
    out_file = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:", ["ofile="])
    except getopt.GetoptError:
        print("test.py -o <output file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("test.py -o <output file>")
            sys.exit()
        elif opt in ("-o", "--ofile"):
            out_file = Path(arg)
            out_file.parent.mkdir(parents=True, exist_ok=True)
    main(out_file)
