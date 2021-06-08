trmmDir='/Barracuda/USERS/forecast/ewb/trmm'

'sdfopen 'trmmDir'/trmm_24hr_acc.nc'
'sdfopen 'trmmDir'/trmm_48hr_acc.nc'

'setLoc_SEA'

'set dfile 1'
'set t 1'
'set geotiff 'trmmDir'/latest_trmm_24hr-total.tif'
'set gxout geotiff'
'd precipitation'
'c'

'set dfile 2'
'set t 1'
'set geotiff 'trmmDir'/latest_trmm_48hr-total.tif'
'set gxout geotiff'
'd precipitation'
'c'

'quit'
