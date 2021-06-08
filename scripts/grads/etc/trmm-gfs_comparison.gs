date='2018-10-16_02PhT'
d12title='2018-10-16:02 to 2018-10-16:14 PhT'
d24title='2018-10-16:02 to 2018-10-17:02 PhT'
d48title='2018-10-16:02 to 2018-10-18:02 PhT'
d72title='2018-10-16:02 to 2018-10-19:02 PhT'
outdir='/Barracuda/USERS/forecast/scripts/../output'
hh=18
yyyymmdd=20181015

'sdfopen trmm_files/trmm_12hr_acc.nc'
'sdfopen trmm_files/trmm_24hr_acc.nc'
'sdfopen trmm_files/trmm_48hr_acc.nc'
'sdfopen trmm_files/trmm_48hr_acc.nc'
'sdfopen http://nomads.ncep.noaa.gov/dods/gfs_0p25_1hr/gfs'yyyymmdd'/gfs_0p25_1hr_'hh'z'

'set mpdset hires'
'set display color white'
'c'
'set grid off'
'set gxout shaded'
'setLoc_PH'

'c'
'set dfile 1'
'set t 1'
'set z 1'
'define p12trmm=precipitation'
'define p12trmm=re(p12trmm,0.25)'
'set dfile 5'
'set t 1'
'set z 1'
'define p12gfs=sum(apcpsfc,t=7,t=13,6)'
'define p12gfs=re(p12gfs,0.25)'
'define p12diff=p12gfs-p12trmm'
say Saving 12hr diff image...
'set grads off'
'set mpdraw off'
'setColor_diff'
'd p12diff'
'draw shp world_shp/country.shp'
'draw title GFS(0.25 degree)-TRMM(0.25 degree)\Difference Initialized from 'date'\12-Hr Total Rainfall(mm) 'd12title
'cbarn'
'printim 'outdir'/trmm-gfs_12hr_asof'date'.gif'
'define rmse=sqrt(aave(pow(p12diff,2),lon=112, lon=131, lat=4, lat=22))'
'd rmse'
rmse=subwrd(result,4)
'define mb=aave(p12diff,lon=112, lon=131, lat=4, lat=22)'
'd mb'
mb=subwrd(result,4)
'define scorr1=scorr(p12gfs,p12trmm,lon=112, lon=131, lat=4, lat=22)'
'd scorr1'
scorr=subwrd(result,4)
write('fcst_verify.csv', '12hr, 'd12title', GFS, 'rmse','mb','scorr, append) 

'c'
'set dfile 2'
'set t 1'
'set z 1'
'define p24trmm=precipitation'
'define p24trmm=re(p24trmm,0.25)'
'set dfile 5'
'set t 1'
'set z 1'
'define p24gfs=sum(apcpsfc,t=7,t=25,6)'
'define p24gfs=re(p24gfs,0.25)'
'define p24diff=p24gfs-p24trmm'
say Saving 24hr diff image...
'set grads off'
'set mpdraw off'
'setColor_diff'
'd p24diff'
'draw shp world_shp/country.shp'
'draw title GFS(0.25 degree)-TRMM(0.25 degree)\Difference Initialized from 'date'\24-Hr Total Rainfall(mm) 'd24title
'cbarn'
'printim 'outdir'/trmm-gfs_24hr_asof'date'.gif'
'define rmse=sqrt(aave(pow(p24diff,2),lon=112, lon=131, lat=4, lat=22))'
'd rmse'
rmse=subwrd(result,4)
'define mb=aave(p24diff,lon=112, lon=131, lat=4, lat=22)'
'd mb'
mb=subwrd(result,4)
'define scorr2=scorr(p24gfs,p24trmm,lon=112, lon=131, lat=4, lat=22)'
'd scorr2'
scorr=subwrd(result,4)
write('fcst_verify.csv', '24hr, 'd24title', GFS, 'rmse','mb','scorr, append) 

'c'
'set dfile 3'
'set t 1'
'set z 1'
'define p48trmm=precipitation'
'define p48trmm=re(p48trmm,0.25)'
'set dfile 5'
'set t 1'
'set z 1'
'define p48gfs=sum(apcpsfc,t=7,t=49,6)'
'define p48gfs=re(p48gfs,0.25)'
'define p48diff=p48gfs-p48trmm'
say Saving 48hr diff image...
'set grads off'
'set mpdraw off'
'setColor_diff'
'd p48diff'
'draw shp world_shp/country.shp'
'draw title GFS(0.25 degree)-TRMM(0.25 degree)\Difference Initialized from 'date'\48-Hr Total Rainfall(mm) 'd48title
'cbarn'
'printim 'outdir'/trmm-gfs_48hr_asof'date'.gif'
'define rmse=sqrt(aave(pow(p48diff,2),lon=112, lon=131, lat=4, lat=22))'
'd rmse'
rmse=subwrd(result,4)
'define mb=aave(p48diff,lon=112, lon=131, lat=4, lat=22)'
'd mb'
mb=subwrd(result,4)
'define scorr3=scorr(p48gfs,p48trmm,lon=112, lon=131, lat=4, lat=22)'
'd scorr3'
scorr=subwrd(result,4)
write('fcst_verify.csv', '48hr, 'd48title', GFS, 'rmse','mb','scorr, append) 

'c'
'set dfile 4'
'set t 1'
'set z 1'
'define p72trmm=precipitation'
'define p72trmm=re(p72trmm,0.25)'
'set dfile 5'
'set t 1'
'set z 1'
'define p72gfs=sum(apcpsfc,t=7,t=73,6)'
'define p72gfs=re(p72gfs,0.25)'
'define p72diff=p72gfs-p72trmm'
say Saving 72hr diff image...
'set grads off'
'set mpdraw off'
'setColor_diff'
'd p72diff'
'draw shp world_shp/country.shp'
'draw title GFS(0.25 degree)-TRMM(0.25 degree)\Difference Initialized from 'date'\72-Hr Total Rainfall(mm) 'd72title
'cbarn'
'printim 'outdir'/trmm-gfs_72hr_asof'date'.gif'
'define rmse=sqrt(aave(pow(p72diff,2),lon=112, lon=131, lat=4, lat=22))'
'd rmse'
rmse=subwrd(result,4)
'define mb=aave(p72diff,lon=112, lon=131, lat=4, lat=22)'
'd mb'
mb=subwrd(result,4)
'define scorr4=scorr(p72gfs,p72trmm,lon=112, lon=131, lat=4, lat=22)'
'd scorr4'
scorr=subwrd(result,4)
write('fcst_verify.csv', '72hr, 'd72title', GFS, 'rmse','mb','scorr, append) 

'quit'


