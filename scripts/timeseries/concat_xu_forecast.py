#!/usr/bin/env python
# coding: utf-8

yyyymmdd = '2021-05-14'
init = '02'
OUT_DIR = "/home/modelman/forecast/output/timeseries"

#combine variables  rain, rh, t2 in one csv
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"Concatinating forecast data at {yyyymmdd}_{init}PHT...")

df_rain = pd.read_csv(f'csv/{yyyymmdd}_{init}PHT_xuws2_rain.csv',names=['PR'])
df_rh   = pd.read_csv(f'csv/{yyyymmdd}_{init}PHT_xuws2_rh.csv',names=['RH'])
df_t2   = pd.read_csv(f'csv/{yyyymmdd}_{init}PHT_xuws2_t2.csv',names=['T'])
df_psfc = pd.read_csv(f'csv/{yyyymmdd}_{init}PHT_xuws2_psfc.csv',names=['PSFC'])
df_ws10 = pd.read_csv(f'csv/{yyyymmdd}_{init}PHT_xuws2_ws10.csv',names=['WS10'])
df_wd10 = pd.read_csv(f'csv/{yyyymmdd}_{init}PHT_xuws2_wd10.csv',names=['WD10'])
df_u10  = pd.read_csv(f'csv/{yyyymmdd}_{init}PHT_xuws2_u10.csv',names=['U10'])
df_v10  = pd.read_csv(f'csv/{yyyymmdd}_{init}PHT_xuws2_v10.csv',names=['V10'])

frames = [df_rain,df_rh,df_t2,df_psfc,df_ws10,df_wd10,df_u10,df_v10]
result = pd.concat(frames, axis=1)

#NOTE: the missing value is replaced to 0 for now (2021 May 05 - gela)
#result= result.replace(-999000000.0,0)

out_file = Path(OUT_DIR) / f'csv/xuws2_forecast_{yyyymmdd}_{init}PHT.csv'
out_file.parent.mkdir(parents=True,exist_ok=True)
result.to_csv(str(out_file), index=False)
