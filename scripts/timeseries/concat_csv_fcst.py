#!/usr/bin/env python
# coding: utf-8

yyyymmdd = '2021-06-20'
init = '20'
OUT_DIR = '/home/modelman/forecast/output/timeseries/csv/20210620/12'
IN_DIR = '/home/modelman/forecast/scripts/timeseries'
#combine variables  rain, rh, t2 in one csv
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_stat = pd.read_csv(Path(IN_DIR) / f'csv/station_id.csv',names=['stations'])
stations = df_stat['stations'].tolist()
for i in stations:

    print(f"Concatinating forecast data at {yyyymmdd}_{init}PHT...")
    print(f'Station {i}')
    df_rain = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_rain.csv',names=['PR'])
    df_rh   = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_rh.csv',names=['RH'])
    df_t2   = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_t2.csv',names=['T'])
    #df_pressure = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_pressure.csv',names=['PSFC'])
    df_ws10 = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_ws10.csv',names=['WS10'])
    df_wd10 = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_wd10.csv',names=['WD10'])
    df_u10m  = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_u10m.csv',names=['U10'])
    df_v10m  = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_v10m.csv',names=['V10'])
    df_ghi  = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_ghi.csv',names=['GHI'])
    df_wp  = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_windpow.csv',names=['WINDPOW'])

    #frames = [df_rain,df_rh,df_t2,df_pressure,df_ws10,df_wd10,df_u10m,df_v10m,df_ghi,df_wp]
    frames = [df_rain,df_rh,df_t2,df_ws10,df_wd10,df_u10m,df_v10m,df_ghi,df_wp]
    result = pd.concat(frames, axis=1)

    #NOTE: the missing value is replaced to 0 for now (2021 May 05 - gela)
    #result= result.replace(-999000000.0,0)

    out_file = Path(OUT_DIR) / f'{i}_forecast_{yyyymmdd}_{init}PHT.csv'
    out_file.parent.mkdir(parents=True,exist_ok=True)
    result.to_csv(str(out_file), index=False)
