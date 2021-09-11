date='2021-07-13_08PHT'
d1title='2021-07-13_08 to 2021-07-14_08 PHT'
d2title='2021-07-14_08 to 2021-07-15_08 PHT'
d3title='2021-07-15_08 to 2021-07-16_08 PHT'
d4title='2021-07-16_08 to 2021-07-17_08 PHT'
d5title='2021-07-17_08 to 2021-07-18_08 PHT'
*outdir='/home/modelman/forecast/output/maps'
outdir='/home/modelman/forecast/scripts/rainchance/test'
wrfres='5'
date2='2021-07-13_08 PHT'

'sdfopen /home/modelman/forecast/model/ENSEMBLE/wrffcst_d01_2021-07-13_00_ens.nc'

shpsrc='/home/modelman/forecast/scripts/shp'

len = 0.2
scale = 5
xrit = 7.8
ybot = 3.9
'set rgb 75 75 75 75'
'sdfopen /home/modelman/forecast/scripts/rainchance/nc/rainchance_day1_'date'.nc'
'set dfile 2'
'set z 1'
'set t 1'
'define day1 = chance'
'close 2'
'set dfile 1'

*-------------------------------------------------------*
* GET TIFF FILES OF PRECIPITATION
*-------------------------------------------------------*

*'setLoc_PH'
*'set t 13'
*'set geotiff 'outdir'/../tif/wrf-12hr_rain_'date'.tif'
*'set gxout geotiff'
*'d rainc+rainnc'
*'c'

*'set t 25'
*'set geotiff 'outdir'/../tif/wrf-24hr_rain_'date'.tif'
*'set gxout geotiff'
*'d rainc+rainnc'
*'c'

*'set t 49'
*'set geotiff 'outdir'/../tif/wrf-48hr_rain_'date'.tif'
*'set gxout geotiff'
*'d rainc+rainnc'
*'c'

*'set t 73'
*'set geotiff 'outdir'/../tif/wrf-72hr_rain_'date'.tif'
*'set gxout geotiff'
*'d rainc+rainnc'
*'c'

'set mpdset hires'
'set display color white'
'c'
'set grid off'
'set gxout shaded'
'set lat 5 20'
'set lon 116 128'
'set xlint 5'
'set ylint 5'
*-------------------------------------------------------*
* PLOT 24HR MAPS
*-------------------------------------------------------*
say Processing 24hr forecast...
'set t 25'
'set z 1'
'define p24=rainc+rainnc'
'set z 4'
'define w24mag=mag(u,v)'
say Saving 24hr forecast image...
'c'
'set xlint 5'
'set ylint 5'
'set grads off'
'set mpdraw off'
'set parea 0.25 8.25 1.5 10.25'
'setColor_gsmap'
'set z 1'
'd p24'
'set line 15 1 5'
'draw shp 'shpsrc'/world_shp/country.shp'

'set string 1 c 5.5 0'
'set strsiz 0.075'
'draw string 4.25 0.8 WRF Ensemble Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 24-Hr Total Rainfall(mm)'
'draw string 4.25 10.6 Valid from 'd1title''
'cbarn 1 1 7.5 6'
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.5 8.85 [mm]'

'set tile 1 2 6 6 3 0'
'set rgb 22 tile 1'
'set clevs 2'
'set ccols -1 22'
'd day1'

'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 2.33 1.79 observatory.ph'

'gxprint 'outdir'/wrf-24hr_rain_'date'.png'


'quit'
