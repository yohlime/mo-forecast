date='2021-09-10_08PHT'
date2='2021-09-10_08 PHT'
date3='2021-09-10_00'
outdir='/home/modelman/forecast/output/validation/20210910/00'
data='gauge'
'sdfopen /home/modelman/forecast/validation/gsmap/nc/gsmap_'data'_'date3'.nc'

shpsrc='/home/modelman/forecast/scripts/shp'

if (data='gauge')
datalabel='GSMaP_NRT (Gauge-Calibrated)'
endif
if (data='nrt')
datalabel='GSMaP_NRT'
endif
if (data='now')
datalabel='GSMaP_NOW'
endif
*-------------------------------------------------------*
* PLOT RAINFALL MAP
*-------------------------------------------------------*
say 'Saving 24hr GSMaP image...'
'setMap'
'set lat 5 20'
'set lon 116 128'
'setColor_gsmap'
'set gxout grfill'
'd precip'
'set line 1 1 5'
'draw shp 'shpsrc'/world_shp/country.shp'
'set string 1 c 5.5 0'
'set strsiz 0.075'
'draw string 4.25 0.8 'datalabel' at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 GSMaP 24-Hr Total Rainfall(mm)'
'draw string 4.25 10.6 From 'date2''
'cbarn 1 1 7.5 6'
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.5 8.85 [mm]'
'setLabel_MO'
'draw string 2.33 1.79 observatory.ph'

**Print
'gxprint 'outdir'/gsmap-24hr_rain_day1_'date'.png'

** save 24hr data
'define rsum = precip'
'set sdfwrite nc/gsmap_24hr_rain_day1_'date'.nc'
'sdfwrite rsum'

'quit'
