#!/usr/bin/env python
# coding: utf-8

#get the climatological heat index of MO station (2010-2019)
#change initialization and variables for automation
#yyyymmdd and init are in local time (PHT)
#mm = choose climatological month
yyyymmdd = '2021-06-08'
init = '08'
mm = 6
OUT_DIR = "/home/modelman/forecast/output/timeseries"

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"Reading forecast data at {yyyymmdd}_{init}PHT...")
df=pd.read_csv(Path(OUT_DIR) / f"csv/MOIP_forecast_{yyyymmdd}_{init}PHT.csv",na_values='-999000000')

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
#x_range=pd.date_range(f'{yyyymmdd}-{init}',periods=73, freq='H').strftime('%m-%d %H:00')
x_range=pd.date_range(f'{yyyymmdd}-{init}',periods=73, freq='H').strftime('%a %H:00')
y_range=np.array([10 for x in range(73)])
x_range2=pd.date_range(f'{yyyymmdd}-{init}',periods=73, freq='H').strftime('%A %b %-d')

print("plotting time series plots...")
#plot into 4 panels 1 column
plt.figure(dpi=300)
plt.rcParams["figure.figsize"] = (19,9)
fig, (ax1,ax3,ax2,ax6) = plt.subplots(ncols=1,nrows=4)
if init == '20':
    ax3.text(12, 81, x_range2[12], fontsize=16,ha='center')
    ax3.text(36, 81, x_range2[36], fontsize=16,ha='center')
    ax3.text(60, 81, x_range2[60], fontsize=16,ha='center')
else:
    ax3.text(12, 81, x_range2[0], fontsize=16,ha='center')
    ax3.text(36, 81, x_range2[24], fontsize=16,ha='center')
    ax3.text(60, 81, x_range2[48], fontsize=16,ha='center')

#plot rainfall
ax1.axvline(x=0, ymin=-0.1, ymax=5, linestyle='dotted', color='gray', label='Day 1')
ax1.axvline(x=24, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 2')
ax1.axvline(x=48, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 3')
ax1.bar(x_range, PR_dat, edgecolor='blue', facecolor='none',linewidth=3)
ax1.set_xticks(np.arange(0, len(x_range)+1, 6))
#ax1.plot(x_range, y_range, color='blue')
ax1.set_xlim([-2,73])
ax1.set_ylim([-0.1, 5])
ax1.tick_params(axis='x', labelsize=8)
ax1.set_xticklabels([])
ax1.tick_params(axis='y', labelsize=12)
ax1.set_title(f'Forecast (Manila Observatory)\nInitialized at {yyyymmdd} {init}:00 PHT',
              pad=38,fontsize=18)
ax1.set_ylabel("Rainfall (mm/hr)",size=12,color='blue')


#plot relative humidity
#ax2 = ax1.twinx()
ax2.axvline(x=0, ymin=-0.1, ymax=5, linestyle='dotted', color='gray', label='Day 1')
ax2.axvline(x=24, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 2')
ax2.axvline(x=48, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 3')
ax2.plot(x_range, RH_dat, '-', color='green', marker='.', linewidth=3,markersize=12,label='Relative Humidity')
ax2.set_xticks(np.arange(0, len(x_range)+1, 6))
ax2.set_xlim([-2,73])
ax2.set_ylim([20, 100])
ax2.tick_params(axis='x', labelsize=8)
ax2.set_xticklabels([])
ax2.tick_params(axis='y', labelsize=12)
ax2.set_ylabel("Relative Humidity (%)",size=12,color='green')

#plot temperature
ax3.axvline(x=0, ymin=-0.1, ymax=5, linestyle='dotted', color='gray',)
ax3.axvline(x=24, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )
ax3.axvline(x=48, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )
ax3.plot(x_range, HI, '-', color='purple',marker='.', linewidth=3,markersize=12,label='Heat Index')
ax3.plot(x_range, T_dat, '-', color='red', marker='.', linewidth=3,markersize=12,label='Temperature')
ax3.set_xticks(np.arange(0, len(x_range)+1, 6))
ax3.set_xlim([-2,73])
ax3.set_ylim([25, 50])
ax3.tick_params(axis='x', labelsize=8)
ax3.set_xticklabels([])
ax3.tick_params(axis='y', labelsize=12)
ax3.legend(loc='upper right')
ax3.set_ylabel("Temperature (°C)",size=12,color='red')


#plot heat index
#ax4 = ax3.twinx()
#ax4.plot(x_range, HI, '-', color='brown',marker='.', label='Heat Index')
#ax4.set_xticks(np.arange(0, len(x_range)+1, 6))
#ax4.set_ylim([25,45])
#ax4.tick_params(axis='x', labelsize=8)
#ax4.tick_params(axis='y', labelsize=12)
#ax4.legend(loc='upper right')
#ax4.set_ylabel("Heat Index (°C)",size=12,color='brown')


#plot pressure
#ax5.plot(x_range, PRES_dat, '-', color='black', marker='.',  label='Pressure')
#ax5.set_xticks(np.arange(0, len(x_range)+1, 6))
#ax5.set_ylim([1000, 1010])
#ax5.tick_params(axis='x', labelsize=8)
#ax5.tick_params(axis='y', labelsize=10)
#ax5.set_ylabel("Pressure (hPa)",size=10,color='black')

#plot wind speed and wind barbs
ax6.axvline(x=0, ymin=-0.1, ymax=5, linestyle='dotted', color='gray', label='Day 1')
ax6.axvline(x=24, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 2')
ax6.axvline(x=48, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 3')
ax6.plot(x_range, WS10_dat, '-', color='black', marker='.', linewidth=3,markersize=12,)
#ax6.barbs(x_range, 10, U10_dat,V10_dat,WS10_dat,color='black',flagcolor='r',
#                 barbcolor=['b', 'g'], length=6,linewidth=2,sizes=dict(emptybarb=0.005, spacing=.1, height=0.5))
#ax6.arrow(x_range, y_range, U10_dat,V10_dat,ec='black',
#                  head_width=0.08, head_length=0.08)
U10_dat = (U10_dat / np.sqrt(U10_dat**2 + V10_dat**2))
V10_dat = (V10_dat / np.sqrt(U10_dat**2 + V10_dat**2))
ax6.quiver(x_range, y_range,U10_dat,V10_dat, width=0.001,color='black',units='width',scale=50,headwidth=5)

ax6.set_xticks(np.arange(0, len(x_range)+1, 6))
ax6.set_xlim([-2,73])
ax6.set_ylim([0, 20])
ax6.tick_params(axis='x', labelsize=12, labelrotation=30)
ax6.tick_params(axis='y', labelsize=12)
ax6.set_ylabel("Wind Speed (m/s)",size=12,color='black')
ax6.set_xlabel("Day and Time (PHT)",size=12)

print("done!")
print("Saving figure...")

out_file = Path(OUT_DIR) / f'img/forecast_{yyyymmdd}_{init}PHT.png'
out_file.parent.mkdir(parents=True,exist_ok=True)
plt.savefig(str(out_file), dpi=300,bbox_inches='tight')
print("done!")
