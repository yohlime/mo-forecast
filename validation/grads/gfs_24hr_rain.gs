date='2021-09-10_08PHT'
date2='2021-09-10_08 PHT'
date3='2021-09-10_00'
outdir='/home/modelman/forecast/output/validation/20210910/00'
gfsdir='/home/modelman/forecast/validation/gfs/nc/20210910/00'
shpsrc='/home/modelman/forecast/scripts/shp'

tt=1
tmax=24
while (tt <= tmax)

if (tt <= 9)
'sdfopen 'gfsdir'/GFS00'tt'_pr.nc'
else
'sdfopen 'gfsdir'/GFS0'tt'_pr.nc'
endif

'define rain'tt'= pr'
say 'rain'tt''
'close 1'
tt=tt+1
endwhile
tt=1
'sdfopen 'gfsdir'/GFS00'tt'_pr.nc'
'define rainsum= rain1+rain2+rain3+rain4+rain5+rain6+rain7+rain8+rain9+rain10+rain11+rain12+rain13+rain14+rain5+rain16+rain17+rain18+rain19+rain20+rain21+rain22+rain23+rain24'
**Set up plotting resources

*-------------------------------------------------------*
* PLOT RAINFALL MAP
*-------------------------------------------------------*
say 'Saving 24hr GFS image...'
'setMap'
'set lat 5 20'
'set lon 116 128'
'setColor_gsmap'
'set gxout grfill'
'define rsum=rainsum*3600'
'd rsum'

'set line 1 1 5'
'draw shp 'shpsrc'/world_shp/country.shp'
'set string 1 c 5.5 0'
'set strsiz 0.075'
'draw string 4.25 0.8 GFS Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 GFS 24-Hr Total Rainfall(mm)'
'draw string 4.25 10.6 Valid from 'date2''
'cbarn 1 1 7.5 6'
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.5 8.85 [mm]'
'setLabel_MO'
'draw string 2.33 1.79 observatory.ph'

**Print
'gxprint 'outdir'/gfs-24hr_rain_day1_'date'.png'

** save 24hr data
'set sdfwrite nc/gfs_24hr_rain_day1_'date'.nc'
'sdfwrite rsum'

'quit'
