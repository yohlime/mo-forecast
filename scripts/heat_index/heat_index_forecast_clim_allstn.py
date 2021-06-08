#!/usr/bin/env python
#get the climatological heat index of MO station (2010-2019)
#change initialization and variables for automation
#yyyymmdd and init are in local time (PHT)
#mm = choose climatological month
yyyymmdd='2021-04-29'
init='02'
mm = 4

stations = ["MOIP","mo001","mo004","makati01","makati02","makati03","makati04","makati05","makati06",\
        "mw001","mw002","mw003","mw004","mw006","mw007","mw008","mw009","mw010","mw011","mw012","mw013",\
        "mw014","mw015","mw016","mw017","mw018","makati07","mw028","Shell023"]
stations = ["MOIP"]
for stn in stations:
    print ("computing for heat index over {0} at {1}_{2} PHT".format(stn,yyyymmdd,init))

    ################################################
    #     for computing foreacast heat index
    ################################################
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import math

    dat=pd.read_csv("csv/MOIP_data_{0}_{1}PHT.csv".format(yyyymmdd,init))
    df = pd.DataFrame(dat)
    df['T_V2'] = df['T']-273.15

    RH_dat = np.array(df['RH'],dtype=float)
    T_dat = np.array(df['T_V2'],dtype=float)

    def calculate_heat_index(t,rh):
        t_fahrenheit = t * (9./5.) + 32

        heat_index_fahrenheit = -42.379 + (2.04901523 * t_fahrenheit) + (10.14333127 * rh) +(-0.22475541 * t_fahrenheit * rh) + (-0.006837837 * t_fahrenheit * t_fahrenheit) +         (-0.05481717 * rh * rh) + (0.001228747 * t_fahrenheit * t_fahrenheit * rh) + (0.00085282 * t_fahrenheit * rh * rh) + (-0.00000199 * t_fahrenheit * t_fahrenheit * rh * rh)
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
            heat_index[locs] = -999
        locs = np.ma.where(rh < 40.0)
        if len(locs[0]) > 0:
            heat_index[locs] = -999
        return heat_index

    HI=calculate_heat_index(T_dat,RH_dat)
#    HI= np.where(HI== -99., np.nan,HI) 

    print ("done computing forecast heat index!")

    ################################################
    #        store heat index forecast data
    ################################################
    x_range=pd.date_range(f'{yyyymmdd}-{init}',periods=72, freq='H').strftime('%Y-%m-%d-%H')

    def round_up(n, decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n*multiplier + 0.5) / multiplier

    ru_RH = [round_up(n, 0) for n in df['RH']]
    ru_T  = [round_up(n, 0) for n in df['T_V2']]
    ru_HI = [round_up(n, 0) for n in HI]

    ru_RH = [math.trunc(n) for n in ru_RH]
    ru_T =  [math.trunc(n) for n in ru_T]
    ru_HI = [math.trunc(n) for n in ru_HI]
    
    df['Date'] = x_range
    df['RH'] = ru_RH
    df['T'] = ru_T
    df['HI'] = ru_HI
    df_new = df[['Date','RH','T','HI']]
    df_new.to_csv('/home/modelman/forecast/output/heat_index/csv/hi_forecast_{0}_{1}_{2}PHT.csv'.format(stn,yyyymmdd, init), index=False)

    print ("done saving the hourly heat index in all stations!")

