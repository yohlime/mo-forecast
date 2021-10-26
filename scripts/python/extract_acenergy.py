from pathlib import Path
import pandas as pd
import xarray as xr

from __const__ import tz, script_dir

site_df = pd.read_csv(script_dir / "python/resources/csv/acenergy.csv")

def extract_acenergy(ds_dict, out_dir):
    init_dt = pd.to_datetime(
        list(ds_dict.values())[0].time.values[0], utc=True
    ).astimezone(tz)
    ds = ds_dict
    _ds = []

    # # region ppv
    # print("Processing ppv...")

    # da = ds["ppv"].mean("ens")
    # da.name = "solPow"
    # _ds.append(da)
    # da = ds["ppv"].min("ens")
    # da.name = "solPowMin"
    # _ds.append(da)
    # da = ds["ppv"].max("ens")
    # da.name = "solPowMax"
    # _ds.append(da)
    # # end region ppv

    # region ghi
    print("Processing ghi...")

    da = ds["ghi"].mean("ens")
    da.name = "GHIMean"
    _ds.append(da)
    da = ds["ghi"].min("ens")
    da.name = "GHIMin"
    _ds.append(da)
    da = ds["ghi"].max("ens")
    da.name = "GHIMax"
    _ds.append(da)
    # end region ghi

    new_ds = xr.merge(_ds)
    ds = new_ds
    out_df = []
    for idx, r in site_df.iterrows():
        # df_dict = {}
        
        _df = ds.sel(lon=r["lon"], lat=r["lat"], method="nearest").to_dataframe()
        _df.drop(columns=["lon", "lat"], inplace=True)
        _df.reset_index(inplace=True)
        _df.rename(columns={"time": "timestamp"}, inplace=True)
        _df["timestamp"] = (
            _df["timestamp"]
            .dt.tz_localize("UTC")
            .dt.tz_convert(tz)
            .dt.strftime("%Y-%m-%dT%H:00:00")
        )
        
        stnid = r['name']
        out_df = pd.DataFrame(_df[["timestamp","GHIMean","GHIMin","GHIMax"]])
        out_file = Path(out_dir) / f"acenergy_{stnid}_{init_dt.strftime('%Y-%m-%d_%H')}PHT.csv"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_df.to_csv(str(out_file),index=False, float_format='%.2f')