date='2018-10-19_08PhT'
d12title='2018-10-19:08 to 2018-10-19:20 PhT'
d24title='2018-10-19:08 to 2018-10-20:08 PhT'
d48title='2018-10-19:08 to 2018-10-21:08 PhT'
d72title='2018-10-19:08 to 2018-10-22:08 PhT'
outdir='/Barracuda/USERS/forecast/scripts/../output'
wrfres='25'

'open /Barracuda/USERS/forecast/scripts/WRF/ARWpost/fcst/wrffcst_d01_2018-10-19_00.ctl'
'sdfopen http://nomads.ncep.noaa.gov/dods/gfs_0p25_1hr/gfs20181019/gfs_0p25_1hr_00z'

'set mpdset hires'
'set display color white'
'c'
'set grid off'
'set gxout shaded'
'setLoc_PH'

'set dfile 1'
'set t 13'
'define p12wrf=rainc+rainnc'
'define p12wrf=re(p12wrf,0.'wrfres')'
'set dfile 2'
'set z 1'
'define p12gfs=sum(apcpsfc,t=7,t=13,6)'
'define p12gfs=re(p12gfs,0.'wrfres')'
'define p12diff=p12wrf-p12gfs'
say Saving 12hr diff image...
'set grads off'
'set mpdraw off'
'setColor_diff'
'd p12diff'
'draw shp world_shp/country.shp'
'draw title WRF('wrfres'km)-GFS(0.25 degree) Regridded to 0.'wrfres' degree\Forecast Difference Initialized from 'date'\12-Hr Total Rainfall(mm) 'd12title
'cbarn'
'printim 'outdir'/wrf-gfs_12hr_rain_'date'.gif'

'c'
'set dfile 1'
'set t 25'
'define p24wrf=rainc+rainnc'
'define p24wrf=re(p24wrf,0.'wrfres')'
'set dfile 2'
'define p24gfs=sum(apcpsfc,t=7,t=25,6)'
'define p24gfs=re(p24gfs,0.'wrfres')'
'define p24diff=p24wrf-p24gfs'
say Saving 24hr diff image...
'set grads off'
'set mpdraw off'
'setColor_diff'
'd p24diff'
'draw shp world_shp/country.shp'
'draw title WRF('wrfres'km)-GFS(0.25 degree) Regridded to 0.'wrfres' degree\Forecast Difference Initialized from 'date'\24-Hr Total Rainfall(mm) 'd24title
'cbarn'
'printim 'outdir'/wrf-gfs_24hr_rain_'date'.gif'

'c'
'set dfile 1'
'set t 49'
'define p48wrf=rainc+rainnc'
'define p48wrf=re(p48wrf,0.'wrfres')'
'set dfile 2'
'define p48gfs=sum(apcpsfc,t=7,t=49,6)'
'define p48gfs=re(p48gfs,0.'wrfres')'
'define p48diff=p48wrf-p48gfs'
say Saving 48hr diff image...
'set grads off'
'set mpdraw off'
'setColor_diff'
'd p48diff'
'draw shp world_shp/country.shp'
'draw title WRF('wrfres'km)-GFS(0.25 degree) Regridded to 0.'wrfres' degree\Forecast Difference Initialized from 'date'\48-Hr Total Rainfall(mm) 'd48title
'cbarn'
'printim 'outdir'/wrf-gfs_48hr_rain_'date'.gif'

'c'
'set dfile 1'
'set t 73'
'define p72wrf=rainc+rainnc'
'define p72wrf=re(p72wrf,0.'wrfres')'
'set dfile 2'
'define p72gfs=sum(apcpsfc,t=7,t=73,6)'
'define p72gfs=re(p72gfs,0.'wrfres')'
'define p72diff=p72wrf-p72gfs'
say Saving 72hr diff image...
'set grads off'
'set mpdraw off'
'setColor_diff'
'd p72diff'
'draw shp world_shp/country.shp'
'draw title WRF('wrfres'km)-GFS(0.25 degree) Regridded to 0.'wrfres' degree\Forecast Difference Initialized from 'date'\72-Hr Total Rainfall(mm) 'd72title
'cbarn'
'printim 'outdir'/wrf-gfs_72hr_rain_'date'.gif'

'quit'