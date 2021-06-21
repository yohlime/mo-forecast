#!/usr/bin/env python
# coding: utf-8

#get the climatological heat index of MO station (2010-2019)
#change initialization and variables for automation
#yyyymmdd and init are in local time (PHT)
#mm = choose climatological month
yyyymmdd = '2021-06-20'
init = '20'
mm = 6
OUT_DIR = '/home/modelman/forecast/output/timeseries'
IN_DIR = '/home/modelman/forecast/output/timeseries/csv/20210620/12'
stn_id = 'MOIP'
station_name = 'Manila Observatory'
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"Reading forecast data at {yyyymmdd}_{init}PHT...")
df=pd.read_csv(Path(IN_DIR) / f'{stn_id}_forecast_{yyyymmdd}_{init}PHT.csv',na_values='-999000000')

#Temperature: convert to celsius
df['T_V2'] = df['T']-273.15

#Surface pressure: convert to hPa
#df['PS_V2'] = df['PSFC']/100

#Wind energy potential: convert from WINDPOW to [MW]
a = 0.5 #constant
p = 1.23 #air density
r = 52 #blade length of turbine (radius)
cp = 0.4 #power coefficient
turb = 4 #assume 4 wind turbines in one hectare
sw_area = 8495 #swept area of turbine

#Wind energy potential equation [MW]
df['WPD'] = turb*(a*p*sw_area*cp*df['WINDPOW'])/1000000

#GHI: convert to [kW/m^2]
df['GHI_V2'] = df['GHI']/1000

#PVOUT: convert from GHI
c1 = -3.75
c2 = df['T_V2']*1.14
c3 = df['GHI']*0.0175
Tcell = c1+c2+c3
Tref = 25
Ncell = 0.12*((df['GHI']*0+1)-0.0045*(Tcell-Tref)+0.1*np.log10(df['GHI']))
spanel = 7200 #estimated solar panel number in 1 hectare
df['PVOUT'] = (df['GHI']*Ncell*spanel)/1000000

#get data from csv
PR_dat   = np.array(df['PR'],dtype=float)
RH_dat   = np.array(df['RH'],dtype=float)
T_dat    = np.array(df['T_V2'],dtype=float)
WS10_dat = np.array(df['WS10'],dtype=float)
WD10_dat = np.array(df['WD10'],dtype=float)
U10_dat  = np.array(df['U10'],dtype=float)
V10_dat  = np.array(df['V10'],dtype=float)
#PRES_dat = np.array(df['PS_V2'],dtype=float)
GHI_dat  = np.array(df['GHI_V2'],dtype=float)
PVOUT_dat  = np.array(df['PVOUT'],dtype=float)
WPD_dat  = np.array(df['WPD'],dtype=float)

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
x_range=pd.date_range(f'{yyyymmdd}-{init}',periods=121, freq='H').strftime('%a %H:00')
y_range=np.array([10 for x in range(121)])
x_range2=pd.date_range(f'{yyyymmdd}-{init}',periods=121, freq='H').strftime('%A %b %-d')

print("plotting time series plots...")
#plot into 6 panels 1 column
plt.figure(dpi=300)
plt.rcParams["figure.figsize"] = (25,25)

fig, (ax1,ax2,ax3,ax4,ax5,ax7) = plt.subplots(ncols=1,nrows=6,constrained_layout=True)

#plot rainfall
ax1.axvline(x=0, ymin=-0.1, ymax=5, linestyle='dotted', color='gray', label='Day 1')
ax1.axvline(x=24, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 2')
ax1.axvline(x=48, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 3')
ax1.axvline(x=72, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 4')
ax1.axvline(x=96, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 5')
ax1.bar(x_range, PR_dat, edgecolor='blue', facecolor='blue')
ax1.set_xticks(np.arange(0, len(x_range)+1, 6))
xmin1, xmax1 = ax1.get_xlim()
ymin1, ymax1 = ax1.get_ylim()
if ymax1 <= 5:
    ax1.axhline(y=1, xmin=xmin1, xmax=xmax1, linestyle='dotted', color='gray')
    ax1.axhline(y=2, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
    ax1.axhline(y=3, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
    ax1.axhline(y=4, xmin=xmin1, xmax=xmax1, linestyle='dotted', color='gray')
    ax1.axhline(y=5, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
else:
    ax1.axhline(y=ymax1*(0.2), xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
    ax1.axhline(y=ymax1*(0.4), xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
    ax1.axhline(y=ymax1*(0.6), xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
    ax1.axhline(y=ymax1*(0.8), xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
#ax1.plot(x_range, y_range, color='blue')
if ymax1 <= 5:
    ymax12 = 5
else:
    ymax12 = ymax1
ax1.set_ylim([-0.1, ymax12])
ax1.set_xlim([-2,121])
ax1.tick_params(axis='x', labelsize=8)
ax1.set_xticklabels([])
ax1.tick_params(axis='y', labelsize=14)
ax1.set_title(f'Forecast ({station_name})\nInitialized at {yyyymmdd} {init}:00 PHT', pad=38,fontsize=18)
ax1.set_ylabel("Rainfall (mm/hr)",size=14,color='blue')

#plot temperature and heat index
ax2.axvline(x=0, ymin=-0.1, ymax=5, linestyle='dotted', color='gray',)
ax2.axvline(x=24, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )
ax2.axvline(x=48, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )
ax2.axvline(x=72, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )
ax2.axvline(x=96, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )
ax2.axhline(y=30, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
ax2.axhline(y=35, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
ax2.axhline(y=40, xmin=xmin1, xmax=xmax1, linestyle='dotted', color='gray')
#ax2.axhline(y=45, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
ax2.plot(x_range, HI, '-', color='purple',marker='.', linewidth=3,markersize=12,label='Heat Index')
ax2.plot(x_range, T_dat, '-', color='red', marker='.', linewidth=3,markersize=12,label='Temperature')
ax2.set_xticks(np.arange(0, len(x_range)+1, 6))
ymin2, ymax2 = ax2.get_ylim()
ax2.set_ylim([25,ymax2])
ax2.set_xlim([-2,121])
ax2.tick_params(axis='x', labelsize=8)
ax2.set_xticklabels([])
ax2.tick_params(axis='y', labelsize=14)
ax2.legend(loc='upper right',fontsize=14)
ax2.set_ylabel("Temperature (°C)",size=14,color='red')

#plot relative humidity
ax3.axvline(x=0, ymin=-0.1, ymax=5, linestyle='dotted', color='gray', label='Day 1')
ax3.axvline(x=24, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 2')
ax3.axvline(x=48, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 3')
ax3.axvline(x=72, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )
ax3.axvline(x=96, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )
ax3.axhline(y=40, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
ax3.axhline(y=60, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
ax3.axhline(y=80, xmin=xmin1, xmax=xmax1, linestyle='dotted', color='gray')
#ax3.bar(x_range, RH_dat, edgecolor='green', facecolor='green',label='Relative Humidity')
ax3.plot(x_range, RH_dat, '-', color='green', marker='.', linewidth=3,markersize=12,label='Relative Humidity')
ax3.set_xticks(np.arange(0, len(x_range)+1, 6))
ax3.set_xlim([-2,121])
ymin3, ymax3 = ax3.get_ylim()
ax3.set_ylim([20, 100])
ax3.tick_params(axis='x', labelsize=8)
ax3.set_xticklabels([])
ax3.tick_params(axis='y', labelsize=14)
ax3.set_ylabel("Relative Humidity (%)",size=14,color='green')

#plot wind speed and wind barbs
ax4.axvline(x=0, ymin=-0.1, ymax=5, linestyle='dotted', color='gray', label='Day 1')
ax4.axvline(x=24, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 2')
ax4.axvline(x=48, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', label='Day 3')
ax4.axvline(x=72, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )
ax4.axvline(x=96, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )
#ax4.bar(x_range, WS10_dat, edgecolor='black', facecolor='black')
ax4.plot(x_range, WS10_dat, '-', color='black', marker='.', linewidth=3,markersize=12,)
#ax6.barbs(x_range, 10, U10_dat,V10_dat,WS10_dat,color='black',flagcolor='r',
#                 barbcolor=['b', 'g'], length=6,linewidth=2,sizes=dict(emptybarb=0.005, spacing=.1, height=0.5))
#ax6.arrow(x_range, y_range, U10_dat,V10_dat,ec='black',
#                  head_width=0.08, head_length=0.08)
U10_dat = (U10_dat / np.sqrt(U10_dat**2 + V10_dat**2))
V10_dat = (V10_dat / np.sqrt(U10_dat**2 + V10_dat**2))
ax4.quiver(x_range, y_range,U10_dat,V10_dat, width=0.001,color='black',units='width',scale=50,headwidth=5)

ax4.set_xticks(np.arange(0, len(x_range)+1, 6))
ax4.set_xlim([-2,121])
ax4.set_ylim([0, 20])
ax4.tick_params(axis='x', labelsize=12)
#ax4.set_xticklabels([])
ax4.tick_params(axis='y', labelsize=14)
ax4.set_ylabel("Wind Speed (m/s)",size=14,color='black')
ax4.set_xlabel("Day and Time (PHT)",size=14)

############### clean energy forecast ##################
########################################################

#plot WPD
ax5.axvline(x=0, ymin=-0.1, ymax=5, linestyle='dotted', color='gray', zorder=0)
ax5.axvline(x=24, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', zorder=0)
ax5.axvline(x=48, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', zorder=0)
ax5.axvline(x=72, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', zorder=0)
ax5.axvline(x=96, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', zorder=0)
ax5.bar(x_range, WPD_dat, edgecolor='red', facecolor='red',label='Wind Power Potential', zorder=1)
#ax5.plot(x_range, WPD_dat, '-', color='blue', marker='.', linewidth=3,markersize=12,label='Wind Power Density (MO)')
ax5.set_xticks(np.arange(0, len(x_range)+1, 6))
ax5.set_xlim([-2,121])
ymin5, ymax5 = ax5.get_ylim()
if ymax5 <= 4:
    ymax52 = 4
else:
    ymax52 = ymax5
ax5.set_ylim([0, ymax52])
#ax5.set_ylim([0, 4])
ax5.tick_params(axis='x', labelsize=12, labelrotation=30)
ax5.set_xticklabels([])
ax5.tick_params(axis='y', labelsize=14)
ax5.set_title(f'Clean Energy Forecast ({station_name})\nInitialized at {yyyymmdd} {init}:00 PHT',
              pad=38,fontsize=18)
ax5.set_ylabel('Wind Power Potential (MW)',size=14,color='black')
ax5.legend(loc='upper right',fontsize=14)
ax5.axhline(y=1, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray', zorder=0)
ax5.axhline(y=2, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray', zorder=0)
ax5.axhline(y=3, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray', zorder=0)
ax5.axhline(y=4, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray', zorder=0)
ax5.axhline(y=5, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray', zorder=0)
ax5.axhline(y=6, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray', zorder=0)

#plot GHI
# ax6.axvline(x=0, ymin=-0.1, ymax=5, linestyle='dotted', color='gray',)
# ax6.axvline(x=24, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )
# ax6.axvline(x=48, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', )

# ax6.plot(x_range, GHI_dat, '-', color='red', marker='.', linewidth=3,markersize=12,label='Global Horizontal Irradiance (MO)')
# ax6.set_xticks(np.arange(0, len(x_range)+1, 6))
# ax6.set_xlim([-2,73])
# ymin6, ymax6 = ax6.get_ylim()
# ax6.set_ylim([0, ymax6])
# ax6.tick_params(axis='x', labelsize=8)
# ax6.set_xticklabels([])
# ax6.tick_params(axis='y', labelsize=14)
# ax6.legend(loc='upper right',fontsize=14)
# #ax6.set_title(f'Solar Energy Forecast (Manila Observatory)\nInitialized at {yyyymmdd} {init}:00 PHT',
# #              pad=38,fontsize=18)
# ax6.set_ylabel("GHI (kW/m$\mathregular{^2}$)",size=14,color='black')
# ax6.axhline(y=ymax6*(0.25), xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
# ax6.axhline(y=ymax6*(0.5), xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray')
# ax6.axhline(y=ymax6*0.75, xmin=xmin1, xmax=xmax1, linestyle='dotted', color='gray')

#plot PVout
ax7.axvline(x=0, ymin=-0.1, ymax=5, linestyle='dotted', color='gray', zorder=0)
ax7.axvline(x=24, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', zorder=0 )
ax7.axvline(x=48, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', zorder=0 )
ax7.axvline(x=72, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', zorder=0 )
ax7.axvline(x=96, ymin=-0.1, ymax=5,linestyle='dotted', color='gray', zorder=0 )
ax7.bar(x_range, PVOUT_dat, edgecolor='goldenrod', facecolor='goldenrod',label='Solar Power Potential',zorder=1)
#ax7.plot(x_range, PVOUT_dat, '-', color='goldenrod', marker='.', linewidth=3,markersize=12,label='Solar Power Potential (MO)')
ax7.set_xticks(np.arange(0, len(x_range)+1, 6))
ax7.set_xlim([-2,121])
ymin7, ymax7 = ax7.get_ylim()
#ax7.set_ylim([0, ymax7])
ax7.set_ylim([0, 2])
ax7.tick_params(axis='x', labelsize=12)
ax7.tick_params(axis='y', labelsize=14)
ax7.legend(loc='upper right',fontsize=14)
ax7.set_ylabel("Solar Power Potential (MW)",size=14,color='black')
ax7.set_xlabel("Day and Time (PHT)",size=14)
ax7.axhline(y=0.5, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray',zorder=0)
ax7.axhline(y=1, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray',zorder=0)
ax7.axhline(y=1.5, xmin=xmin1, xmax=xmax1,linestyle='dotted', color='gray',zorder=0)

ymin1, ymax1 = ax1.get_ylim()
ymin5, ymax5 = ax5.get_ylim()
if ymax1 <=5:
    ymax11 = 5
else:
    ymax11 = ymax1
if ymax5 <=0.1:
    ymax51 = 0.1
else:
    ymax51 = ymax5
if init == '20':
    ax1.text(12, ymax11+(ymax11*0.05), x_range2[12], fontsize=16,ha='center')
    ax1.text(36, ymax11+(ymax11*0.05), x_range2[36], fontsize=16,ha='center')
    ax1.text(60, ymax11+(ymax11*0.05), x_range2[60], fontsize=16,ha='center')
    ax1.text(84, ymax11+(ymax11*0.05), x_range2[84], fontsize=16,ha='center')
    ax1.text(108, ymax11+(ymax11*0.05), x_range2[108], fontsize=16,ha='center')
    ax5.text(12, ymax51+(ymax51*0.05), x_range2[12], fontsize=16,ha='center')
    ax5.text(36, ymax51+(ymax51*0.05), x_range2[36], fontsize=16,ha='center')
    ax5.text(60, ymax51+(ymax51*0.05), x_range2[60], fontsize=16,ha='center')
    ax5.text(84, ymax51+(ymax51*0.05), x_range2[84], fontsize=16,ha='center')
    ax5.text(108, ymax51+(ymax51*0.05), x_range2[108], fontsize=16,ha='center')

else:
    ax1.text(12, ymax11+(ymax11*0.05), x_range2[0], fontsize=16,ha='center')
    ax1.text(36, ymax11+(ymax11*0.05), x_range2[24], fontsize=16,ha='center')
    ax1.text(60, ymax11+(ymax11*0.05), x_range2[48], fontsize=16,ha='center')
    ax1.text(84, ymax11+(ymax11*0.05), x_range2[72], fontsize=16,ha='center')
    ax1.text(108, ymax11+(ymax11*0.05), x_range2[96], fontsize=16,ha='center')
    ax5.text(12, ymax51+(ymax51*0.05), x_range2[0], fontsize=16,ha='center')
    ax5.text(36, ymax51+(ymax51*0.05), x_range2[24], fontsize=16,ha='center')
    ax5.text(60, ymax51+(ymax51*0.05), x_range2[48], fontsize=16,ha='center')
    ax5.text(84, ymax51+(ymax51*0.05), x_range2[72], fontsize=16,ha='center')
    ax5.text(108, ymax51+(ymax51*0.05), x_range2[96], fontsize=16,ha='center')


print("done!")
print("Saving figure...")

out_file = Path(OUT_DIR) / f'img/forecast_{yyyymmdd}_{init}PHT.png'
out_file.parent.mkdir(parents=True,exist_ok=True)
plt.savefig(str(out_file), dpi=300,bbox_inches='tight')
print("done!")
