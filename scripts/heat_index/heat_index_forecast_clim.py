#!/usr/bin/env python
#get the climatological heat index of MO station (2010-2019)
#change initialization and variables for automation
#yyyymmdd and init are in local time (PHT)
#mm = choose climatological month
yyyymmdd='2021-04-29'
init='02'
mm = 4

print ("computing for heat index at {0}_{1} PHT".format(yyyymmdd,init))
################################################
#     for computing foreacast heat index
################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dat=pd.read_csv("csv/MOIP_data_{0}_{1}PHT.csv".format(yyyymmdd,init))
df = pd.DataFrame(dat)
df['T_V2'] = df['T']-273.15

RH_dat = np.array(df['RH'],dtype=float)
T_dat = np.array(df['T_V2'],dtype=float)

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

    locs = np.ma.where(t < 26.6667) # 80F
    if len(locs[0]) > 0:
        heat_index[locs] = -99
    locs = np.ma.where(rh < 40.0)
    if len(locs[0]) > 0:
        heat_index[locs] = -99
    return heat_index

HI=calculate_heat_index(T_dat,RH_dat)
HI= np.where(HI== -99., np.nan,HI) 

print ("done computing forecast heat index!")
################################################
#      get the climatological heat index 
################################################
dat_clim= pd.read_csv(f"climatology/hi_clim_mo_{init}PHT.csv")
df_clim = pd.DataFrame(dat_clim)
clim1 = df_clim.loc[df_clim['Month'] == mm]
clim2 = df_clim.loc[df_clim['Month'] == mm]
clim3 = df_clim.loc[df_clim['Month'] == mm]
frames = [clim1['HI_clim'],clim2['HI_clim'],clim3['HI_clim']]
HI_clim = pd.concat(frames)

print ("done extracting climatological heat index!")

################################################
#        store heat index forecast data
################################################
df['HI'] = HI
df['Month'] = df_clim['Month']
df['Hour'] = df_clim['Hour']
df_new = df[['Month','Hour','RH','T_V2','HI']]
df_new.to_csv('/home/modelman/forecast/output/heat_index/csv/hi_forecast_mo_{0}_{1}PHT.csv'.format(yyyymmdd, init), index=False)


################################################
#            plot HI and HI_clim
################################################

x_range=pd.date_range(f'{yyyymmdd}-{init}',periods=72, freq='H').strftime('%Y-%m-%d-%H')
fig=plt.figure(dpi=300)
plt.plot(x_range, HI_clim.values, '-k.',label='Climatology')
plt.plot(x_range, HI, 'b*', label='Forecast')
plt.xticks(np.arange(0, len(x_range)+1, 24))
plt.ylim([27, 40])
plt.subplots_adjust(right=0.73)
plt.legend(framealpha=1, frameon=True,loc='upper right',prop={'size': 7});
ax = fig.add_subplot(111)
ax.text(91.5, 38, 'Heat Index\nClassification', style='normal', horizontalalignment='center',fontsize=7,)
ax.text(79.45, 36, 'Caution (26.7 to 32.2°C):\n\nFatigue possible with prolonged\nexposure and/or physical activity',
        style='normal', fontsize=5, bbox={'facecolor': 'yellow', 'alpha': 0.5, 'pad': 9.2})
ax.text(79.1, 33, 'Extreme Caution (32.2 to 39.4°C):\n\nHeat stroke, heat cramps,\nor heat exhaustion possible\nwith prolonged exposure\nand/or physical activity',
        style='normal', fontsize=5, bbox={'facecolor': 'orange', 'alpha': 0.5, 'pad': 8})
ax.text(79.85, 29.9, 'Danger (39.4 to 51.1°C):\n\nHeat cramps or heat exhaustion\nlikely and heat stroke possible\nwith prolonged exposure\nand/or physical activity',
        style='normal', fontsize=5, bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10.5})
ax.text(79.5, 28.05, 'Extreme Danger (> 51.1°C):\nHeat stroke highly likely              ',
        style='normal', fontsize=5, bbox={'facecolor': 'red', 'alpha': 0.65, 'pad': 9.4})
plt.title('Forecast Heat Index (MO Station)\nInitialized at {0} {1} PHT'.format(yyyymmdd, init))
plt.xlabel("Date (PHT)")
plt.ylabel("Heat Index (°C)")
plt.savefig('/home/modelman/forecast/output/heat_index/heat_index_{0}_{1}PHT.png'.format(yyyymmdd, init) , dpi=300)
#plt.show()
print ("done plotting heat index graph!")

