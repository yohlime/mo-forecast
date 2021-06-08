date='2018-10-16_02PhT'
d12title='2018-10-16:02 to 2018-10-16:14 PhT'
d24title='2018-10-16:02 to 2018-10-17:02 PhT'
d48title='2018-10-16:02 to 2018-10-18:02 PhT'
d72title='2018-10-16:02 to 2018-10-19:02 PhT'
outdir='/Barracuda/USERS/forecast/scripts/../output'

'sdfopen trmm_files/trmm_12hr_acc.nc'
'sdfopen trmm_files/trmm_24hr_acc.nc'
'sdfopen trmm_files/trmm_48hr_acc.nc'
'sdfopen trmm_files/trmm_72hr_acc.nc'

'set mpdset hires'
'set display color white'
'c'
'set grid off'
'set gxout shaded'
'setLoc_PH'

'c'
'set dfile 1'
'define p12trmm=precipitation'
say Saving 12hr diff image...
'set grads off'
'set mpdraw off'
'setColor_trmm'
'd p12trmm'
'draw shp world_shp/country.shp'
'draw title TRMM(0.25 degree)\12-Hr Total Rainfall(mm) \'d12title
'cbarn'
'printim 'outdir'/trmm_12hr_asof'date'.gif'

'c'
'set dfile 2'
'define p24trmm=precipitation'
say Saving 24hr diff image...
'set grads off'
'set mpdraw off'
'setColor_trmm'
'd p24trmm'
'draw shp world_shp/country.shp'
'draw title TRMM(0.25 degree)\24-Hr Total Rainfall(mm) \'d24title
'cbarn'
'printim 'outdir'/trmm_24hr_asof'date'.gif'

'c'
'set dfile 3'
'define p48trmm=precipitation'
say Saving 48hr diff image...
'set grads off'
'set mpdraw off'
'setColor_trmm'
'd p48trmm'
'draw shp world_shp/country.shp'
'draw title TRMM(0.25 degree)\48-Hr Total Rainfall(mm) \'d48title
'cbarn'
'printim 'outdir'/trmm_48hr_asof'date'.gif'

'c'
'set dfile 4'
'define p72trmm=precipitation'
say Saving 72hr diff image...
'set grads off'
'set mpdraw off'
'setColor_trmm'
'd p72trmm'
'draw shp world_shp/country.shp'
'draw title TRMM(0.25 degree)\72-Hr Total Rainfall(mm) \'d72title
'cbarn'
'printim 'outdir'/trmm_72hr_asof'date'.gif'

'quit'
