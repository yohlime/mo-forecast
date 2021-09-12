date='2021-09-11_08PHT'
date2='2021-09-11_08 PHT'
date3='2021-09-11_00'
outdir='/home/modelman/forecast/output/validation/20210911/00'
wrfdir='nc'
shpsrc='/home/modelman/forecast/scripts/shp'

'sdfopen nc/gsmap_24hr_rain_day1_'date'.nc'
'define obs = re(rsum,0.05,0.05)'
'close 1'

models = 'WRF GFS'
models2 = 'wrf gfs'
i = 1
while (i<=2)
m = subwrd(models,i)
m2 = subwrd(models2,i)
*-------------------------------------------------------*
* PLOT MODEL - GSMAP BIAS MAP
*-------------------------------------------------------*
say 'Saving 24hr 'm'-GSMaP image...'
if (i=1)
'sdfopen 'wrfdir'/wrffcst_d01_'date3'_ens.nc'
'set t 25'
'set lat 5 20'
'set lon 116 128'
'define p24 = rainc+rainnc'
'define model = re(p24,0.05,0.05)'
else
'sdfopen nc/gfs_24hr_rain_day1_'date'.nc'
'set lat 5 20'
'set lon 116 128'
'define model = re(rsum,0.05,0.05)'
endif
'setMap'
'set lat 5 20'
'set lon 116 128'
'setColor_bias'
'set gxout grfill'
'd model-obs'
'set line 1 1 5'
'draw shp 'shpsrc'/world_shp/country.shp'
'set string 1 c 5.5 0'
'set strsiz 0.075'
*'draw string 4.25 0.8 GSMaP_NRT (Gauge-Calibrated) at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 'm'-GSMaP 24-Hr Total Rainfall(mm)'
'draw string 4.25 10.6 From 'date2''
'cbarn 1 1 7.5 6'
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.5 9.15 [mm]'
'setLabel_MO'
'draw string 2.33 1.79 observatory.ph'

**Print
'gxprint 'outdir'/'m2'-gsmap-24hr_rain_day1_'date'.png'
if (i=1)
'set sdfwrite nc/wrf_24hr_rain_day1_'date'.nc'
'sdfwrite p24'
endif
'close 1'
i=i+1
endwhile

'quit'
