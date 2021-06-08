*-----------------------------------
* load data from an opendap server
* your grads installation should suppor opendap
* opendap servers can be found in the NOMADS website:
* http://nomads.ncep.noaa.gov/
*----------------------------------

* USAGE: grads -pbc gfs_rainforecast.gs

*----------------------------------
** EDIT this part   
*----------------------------------
* for yyyymmdd 9am Phil.Time update --> yyyymmdd=yyyymmdd-1day; hh=18 (as of 2am ); date=ddMM2am, where MM=Jan,Feb...
* for yyyymmdd 3pm Phil.Time update --> yyyymmdd=yyyymmdd;      hh=00 (as of 8am ); date=ddMM8am
* for yyyymmdd 9pm Phil.Time update --> yyyymmdd=yyyymmdd;      hh=06 (as of 2pm ); date=ddMM2pm

yyyymmdd=20210223
hh=18
tinit=yyyymmdd''hh

* = local time = UTC + 08
date='2021-02-24_02PhT'
d12title='2021-02-24:02 to 2021-02-24:14 PhT'
d24title='2021-02-24:02 to 2021-02-25:02 PhT'
d48title='2021-02-24:02 to 2021-02-26:02 PhT'
d72title='2021-02-24:02 to 2021-02-27:02 PhT'
outdir='/home/modelman/forecast/output'

*Directory
TCyyyymm='GFS202102'
*WORKDir='/Butanding/USERS/shelec/TC.Updates/'TCyyyymm'/'tinit
*WORKDir='/Barracuda/USERS/Kevin/forecasting/gfs/'TCyyyymm'/'tinit

*'! if [ ! -d 'WORKDir' ]; then mkdir -p 'WORKDir' ; fi'
*'! mkdir 'WORKDir'/maps'
*'! mkdir 'WORKDir'/tif'


*----------------------------------
** START 

'sdfopen http://nomads.ncep.noaa.gov/dods/gfs_0p25_1hr/gfs'yyyymmdd'/gfs_0p25_1hr_'hh'z'

*----------------------------------
* if the data loads successfully then you can use grads command normally
*----------------------------------

*----------------------------------
* options
*----------------------------------
'set mpdset hires'
'set display color white'
'c'
'set grid off'
'set gxout shaded'

*----------------------------------
* set lat lon
*----------------------------------
'setLoc_ewb'

*** plot 12hr acc precip
say Processing 12hr forecast...
'define p12=apcpsfc(t=13)'
say Saving 12hr forecast image...
'c'
'set grads off'
'set mpdraw off'
'setColor'
'd p12'
'draw shp world_shp/country.shp'
'draw title GFS Forecast Initialized from 'date'\12-Hr Total Rainfall(mm)\'d12title
'cbarn 1 0 4.225 1.5'
'printim 'outdir'/gfs-12hr_rain_'date'.png'

*** plot 24hr acc precip
say Processing 24hr forecast...
'define p24=apcpsfc(t=25)'
say Saving 24hr forecast image...
'c'
'set grads off'
'set mpdraw off'
'setColor'
'd p24'
'draw shp world_shp/country.shp'
'draw title GFS Forecast Initialized from 'date'\24-Hr Total Rainfall(mm)\'d24title 
'cbarn 1 0 4.225 1.5'
'printim 'outdir'/gfs-24hr_rain_'date'.png'


*** plot 48hr acc precip
say Processing 48hr forecast...
'define p48=apcpsfc(t=49)'
*'define p48=p24+sum(apcpsfc,t=31,t=49,6)'
say Saving 48hr forecast image...
'c'
'set grads off'
'set mpdraw off'
'setColor'
'd p48'
'draw shp world_shp/country.shp'
'draw title GFS Forecast Initialized from 'date'\48-Hr Total Rainfall(mm)\'d48title
'cbarn 1 0 4.225 1.5'
'printim 'outdir'/gfs-48hr_rain_'date'.png'

*** plot 72hr acc precip
say Processing 72hr forecast...
'define p72=apcpsfc(t=73)'
*'define p72=sum(apcpsfc,t=7,t=73,6)'
say Saving 72hr forecast image...
'c'
'set grads off'
'set mpdraw off'
'setColor'
'd p72'
'draw shp world_shp/country.shp'
'draw title GFS Forecast Initialized from 'date'\72-Hr Total Rainfall(mm)\'d72title
'cbarn 1 0 4.225 1.5'
'printim 'outdir'/gfs-72hr_rain_'date'.png'

*------------------------------*
* SET GEOTIFF for GIS plotting *
'c'
'set geotiff gfs-12hr_rain_'date'.tif'
'set gxout geotiff'
'd p12'

'c'
'set geotiff gfs-24hr_rain_'date'.tif'
'set gxout geotiff'
'd p24'

'c'
'set geotiff gfs-48hr_rain_'date'.tif'
'set gxout geotiff'
'd p48'

'c'
'set geotiff gfs-72hr_rain_'date'.tif'
'set gxout geotiff'
'd p72'

'! mv *.tif 'outdir'/tif'

'quit'
