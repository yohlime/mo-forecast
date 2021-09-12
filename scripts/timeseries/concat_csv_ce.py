#!/usr/bin/env python
# coding: utf-8

yyyymmdd = '2021-09-11'
init = '08'
OUT_DIR = '/home/modelman/forecast/output/summary/clean_energy/20210911/00'
IN_DIR = '/home/modelman/forecast/scripts/timeseries'
#combine variables  rain, rh, t2 in one csv
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
i = 'PH'

print(f"Concatinating clean energy forecast data at {yyyymmdd}_{init}PHT...")
df_st = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_SolarTotal.csv',names=['SolarTotal[MW]'])
df_sm = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_SolarMax.csv',names=['SolarMax[MW]'])
df_sa = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_SolarAve.csv',names=['SolarAve[MW]'])
df_wt = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_WindTotal.csv',names=['WindTotal[MW]'])
df_wm = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_WindMax.csv',names=['WindMax[MW]'])
df_wa = pd.read_csv(Path(IN_DIR) / f'csv/{yyyymmdd}_{init}PHT_{i}_WindAve.csv',names=['WindAve[MW]'])

head = ['Day1','Day2','Day3','Day4','Day5']
df = pd.DataFrame(head,columns=['CleanEnergy'])

frames = [df,df_st,df_sm,df_sa,df_wt,df_wm,df_wa]
result = pd.concat(frames, axis=1)

out_file = Path(OUT_DIR) / f'{i}_cleanenergyfcst_{yyyymmdd}_{init}PHT.csv'
out_file.parent.mkdir(parents=True,exist_ok=True)
result.to_csv(str(out_file), index=False)
