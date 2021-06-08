trmmDir='/Barracuda/USERS/forecast/ewb/trmm/clim'

'sdfopen 'trmmDir'/TRMM.pr.1998-2017.monsum.allyrsmean.nc'
'sdfopen 'trmmDir'/TRMM.pr.1998-2017.daily.allyrsp95.nc'
month=02

'set dfile 1'
'setLoc_SEA'
'set t 'month
'set geotiff 'trmmDir'/latest_trmmClim_monsum_allyrsmean.tif'
'set gxout geotiff'
'd pr'
'c'

'set dfile 2'
'set t 'month
'set geotiff 'trmmDir'/latest_trmmClim_daily_allyrsp95.tif'
'set gxout geotiff'
'd pr'
'c'

'quit'
