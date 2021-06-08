#!/usr/bin/env python
# coding: utf-8

#get the climatological heat index of MO station (2010-2019)
#change initialization and variables for automation
#yyyymmdd and init are in local time (PHT)
#mm = choose climatological month
yyyymmdd = '2021-05-14'
init = '02'
mm = 5
OUT_DIR = "/home/modelman/forecast/output/timeseries"

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"Reading forecast data at {yyyymmdd}_{init}PHT...")
df=pd.read_csv(Path(OUT_DIR) / f"csv/xuws2_forecast_{yyyymmdd}_{init}PHT.csv",na_values='-999000000')

#Temperature: convert to celsius
df['T_V2'] = df['T']-273.15

#Surface pressure: convert to hPa
df['PS_V2'] = df['PSFC']/100

#get data from csv
PR_dat   = np.array(df['PR'],dtype=float)
RH_dat   = np.array(df['RH'],dtype=float)
T_dat    = np.array(df['T_V2'],dtype=float)
WS10_dat = np.array(df['WS10'],dtype=float)
WD10_dat = np.array(df['WD10'],dtype=float)
U10_dat  = np.array(df['U10'],dtype=float)
V10_dat  = np.array(df['V10'],dtype=float)
PRES_dat = np.array(df['PS_V2'],dtype=float)

print("Calculating heat index...")
#heat index function
def calculate_heat_index(t,rh):
    t_fahrenheit = t * (9./5.) + 32

    heat_index_fahrenheit = -42.379 + (2.04901523 * t_fahrenheit) + (10.14333127 * rh) +         (-0.22475541 * t_fahrenheit * rh) + (-0.006837837 * t_fahrenheit * t_fahrenheit) +         (-0.05481717 * rh * rh) + (0.001228747 * t_fahrenheit * t_fahrenheit * rh) +         (0.00085282 * t_fahrenheit * rh * rh) + (-0.00000199 * t_fahrenheit * t_fahrenheit * rh * rh)
    locs = np.ma.where(np.ma.logical_and((rh < 13), (t_fahrenheit > 80), (t_fahrenheit < 112)))
    if len(locs[0]) > 0:
        heat_index_fahrenheit[locs] = heat_index_fahrenheit[locs] - (((13.- rh[locs]) / 4.) * np.ma.sqrt((17. - np.ma.abs(t_fahrenheit[locs] - 95.)) / 17.))
        locs = np.ma.where(np.ma.logical_and((rh > 85), (t_fahrenheit > 80), (t_fahrenheit < 87)))
    if len(locs[0]) > 0:
        heat_index_fahrenheit[locs] = heat_index_fahrenheit[locs] - (((rh[locs ] - 85) / 10.) * ((87. - t_fahrenheit[locs]) / 5.))
    
    locs = np.ma.where(heat_index_fahrenheit < 80)
    if len(locs[0]) > 0:
        heat_index_fahrenheit[locs] = 0.5 * (t_fahrenheit[locs] + 61. + ((t_fahrenheit[locs] - 68.) * 1.2) + (rh[locs] * 0.094))
 
    heat_index = (heat_index_fahrenheit - 32) / (9./5.)

#activate heat index threshold
##    locs = np.ma.where(t < 26.6667) # 80F
##    if len(locs[0]) > 0:
##        heat_index[locs] = -99
##    locs = np.ma.where(rh < 40.0)
##    if len(locs[0]) > 0:
##        heat_index[locs] = -99
    return heat_index

HI=calculate_heat_index(T_dat,RH_dat)
HI= np.where(HI== -99., np.nan,HI) 

#get dates for x-axis labels
x_range=pd.date_range(f'{yyyymmdd}-{init}',periods=73, freq='H').strftime('%m-%d %H:00')
y_range=np.array([0 for x in range(73)])

print("plotting time series plots...")
#plot into 4 panels 1 column
plt.figure(dpi=300)
plt.rcParams["figure.figsize"] = (14,9)
fig, (ax1,ax3,ax5,ax6) = plt.subplots(ncols=1,nrows=4)

#plot rainfall
ax1.bar(x_range, PR_dat, edgecolor='blue', facecolor='none',label='Rainfall')
ax1.set_xticks(np.arange(0, len(x_range)+1, 6))
ax1.plot(x_range, y_range, color='blue')
y_min, y_max = ax1.get_ylim()
ax1.set_ylim([-0.1, y_max])
ax1.tick_params(axis='x', labelsize=8)
ax1.tick_params(axis='y', labelsize=10)
ax1.set_title('Forecast (Xavier University)\nInitialized at {0} {1}:00 PHT'.format(yyyymmdd, init))
ax1.set_ylabel("Rainfall (mm/hr)",size=10,color='blue')

#plot relative humidity
ax2 = ax1.twinx()
ax2.plot(x_range, RH_dat, '-g.', label='Relative Humidity')
ax2.set_xticks(np.arange(0, len(x_range)+1, 6))
y_min, y_max = ax2.get_ylim()
ax2.set_ylim([y_min, 100])
ax2.tick_params(axis='x', labelsize=8)
ax2.tick_params(axis='y', labelsize=10)
ax2.set_ylabel("Relative Humidity (%)",size=10,color='green')

#plot temperature
ax3.plot(x_range, T_dat, '-', color='red', marker='.', label='Temperature')
ax3.set_xticks(np.arange(0, len(x_range)+1, 6))
ax3.set_ylim([20, 40])
ax3.tick_params(axis='x', labelsize=8)
ax3.tick_params(axis='y', labelsize=10)
ax3.set_ylabel("Temperature (°C)",size=10,color='red')

#plot heat index
ax4 = ax3.twinx()
ax4.plot(x_range, HI, '-', color='brown',marker='.', label='Heat Index')
ax4.set_xticks(np.arange(0, len(x_range)+1, 6))
ax4.set_ylim([20, 40])
ax4.tick_params(axis='x', labelsize=8)
ax4.tick_params(axis='y', labelsize=10)
ax4.set_ylabel("Heat Index (°C)",size=10,color='brown')

#plot pressure
ax5.plot(x_range, PRES_dat, '-', color='black', marker='.',  label='Pressure')
ax5.set_xticks(np.arange(0, len(x_range)+1, 6))
y_min, y_max = ax5.get_ylim()
ax5.set_ylim([y_min, y_max])
ax5.tick_params(axis='x', labelsize=8)
ax5.tick_params(axis='y', labelsize=10)
ax5.set_ylabel("Pressure (hPa)",size=10,color='black')

#plot wind speed and wind barbs
ax6.plot(x_range, WS10_dat, '-', color='black', marker='.',  label='Wind Speed')
ax6.barbs(x_range, 10, U10_dat,V10_dat,WS10_dat,color='black',flagcolor='r',
                 barbcolor=['b', 'g'], length=8,sizes=dict(emptybarb=0.0005, spacing=0.2, height=0.5))
ax6.set_xticks(np.arange(0, len(x_range)+1, 6))
ax6.set_ylim([0, 20])
ax6.tick_params(axis='x', labelsize=8)
ax6.tick_params(axis='y', labelsize=10)
ax6.set_ylabel("Wind Speed (m/s)",size=10,color='black')
ax6.set_xlabel("Date (PHT)",size=8)

print("done!")
print("Saving figure...")

out_file = Path(OUT_DIR) / f'img/forecast_xuws2_{yyyymmdd}_{init}PHT.png'
out_file.parent.mkdir(parents=True,exist_ok=True)
plt.savefig(str(out_file), dpi=300,bbox_inches='tight')
print("done!")
