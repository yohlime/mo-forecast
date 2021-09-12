date='2021-09-11_08PHT'
d1title='2021-09-11_08 to 2021-09-12_08 PHT'
d2title='2021-09-12_08 to 2021-09-13_08 PHT'
d3title='2021-09-13_08 to 2021-09-14_08 PHT'
d4title='2021-09-14_08 to 2021-09-15_08 PHT'
d5title='2021-09-15_08 to 2021-09-16_08 PHT'
outdir='/home/modelman/forecast/output/maps'
wrfres='5'
date2='2021-09-11_08 PHT'

'sdfopen /home/modelman/forecast/model/ENSEMBLE/wrffcst_d01_2021-09-11_00_ens.nc'

shpsrc='/home/modelman/forecast/scripts/shp'

*-------------------------------------------------------*
* GET MASK FILE 
*-------------------------------------------------------*
len = 0.2
scale = 5
xrit = 7.8
ybot = 3.9
'set rgb 75 75 75 75'
'sdfopen mask.nc'
'set dfile 2'
'set z 1'
'set t 1'
'define mask = z'
'close 2'
'set dfile 1'
'sdfopen mask_sst.nc'
'set dfile 2'
'set z 1'
'set t 1'
'define masksst = z'
'close 2'
'set dfile 1'

*-------------------------------------------------------*
* GET TIFF FILES OF PRECIPITATION
*-------------------------------------------------------*
hour = '24 48 72 96 120'
hour1 = '25 49 73 97 121'
i=1
while (i<=5)
h=subwrd(hour,i)
h1=subwrd(hour1,i)

* 'setLoc_PH'
* 'set t 'h1''
* 'set geotiff 'outdir'/../tif/wrf-'h'hr_rain_'date'.tif'
* 'set gxout geotiff'
* 'd rainc+rainnc'
* 'c'

i=i+1
endwhile

*-------------------------------------------------------*
* PLOT RAINFALL MAPS
*-------------------------------------------------------*
'set z 1'
hour = '24 48 72 96 120'
timestep = '25 49 73 97 121'
strings = '1 35 69 103 137'
titles = ''d1title''d2title''d3title''d4title''d5title''
i=1
k=0
while (i<=5)
h=subwrd(hour,i)
ts=subwrd(timestep,i)
j=subwrd(strings,i)
t=substr(titles,j,34)
    say 'Saving 24hr rain forecast day'i' image...'
    'set lat 5 20'
    'set lon 116 128'
    'set t 'ts''
    'define p'h'=rainc+rainnc'
    'setMap'
    'setColor_gsmap'
    if (i=1)
    'd p'h''
    else
    prevts=subwrd(hour,k)
    'd p'h' - p'prevts''
    endif
    'set line 1 1 5'
    'draw shp 'shpsrc'/world_shp/country.shp'
    'set string 1 c 5.5 0'
    'set strsiz 0.075'
    'draw string 4.25 0.8 WRF Ensemble Forecast Initialized at 'date2
    'set strsiz 0.15'
    'set string 1 tc 5.5 0'
    'draw string 4.25 10.9 24-Hr Total Rainfall(mm)'
    'draw string 4.25 10.6 Valid from 't''
    'cbarn 1 1 7.5 6'
    'set string 1 c 5.5 0'
    'set strsiz 0.13'
    'draw string 7.5 8.85 [mm]'
    'setLabel_MO'
    'draw string 2.33 1.79 observatory.ph'
    'gxprint 'outdir'/wrf-24hr_rain_day'i'_'date'.png'
k=k+1
i=i+1
endwhile
*-------------------------------------------------------*
* PLOT ACCUMULATED RAINFALL MAPS
*-------------------------------------------------------*
'set z 1'
hour = '24 48 72 96 120'
timestep = '25 49 73 97 121'
strings = '1 35 69 103 137'
titles = ''d1title''d2title''d3title''d4title''d5title''
i=1
while (i<=5)
h=subwrd(hour,i)
ts=subwrd(timestep,i)
j=subwrd(strings,i)
t=substr(titles,j,34)
    say 'Saving rain total forecast day'i' image...'
    'set lat 5 20'
    'set lon 116 128'
    'set t 'ts''
    'define p'h'=rainc+rainnc'
    'setMap'
    'setColor_gsmap'
    'd p'h''
    'set line 1 1 5'
    'draw shp 'shpsrc'/world_shp/country.shp'
    'set string 1 c 5.5 0'
    'set strsiz 0.075'
    'draw string 4.25 0.8 WRF Ensemble Forecast Initialized at 'date2
    'set strsiz 0.15'
    'set string 1 tc 5.5 0'
    'draw string 4.25 10.9 'h'-Hr Total Rainfall(mm)'
    'draw string 4.25 10.6 Valid from 't''
    'cbarn 1 1 7.5 6'
    'set string 1 c 5.5 0'
    'set strsiz 0.13'
    'draw string 7.5 8.85 [mm]'
    'setLabel_MO'
    'draw string 2.33 1.79 observatory.ph'
    'gxprint 'outdir'/wrf-'h'hr_raintotal_'date'.png'
i=i+1
endwhile
*-------------------------------------------------------*
* PLOT WIND MAPS
*-------------------------------------------------------*
'set z 4'
hour = '24 48 72 96 120'
timestep = '25 49 73 97 121'
strings = '1 35 69 103 137'
titles = ''d1title''d2title''d3title''d4title''d5title''
i=1
while (i<=5)
h=subwrd(hour,i)
ts=subwrd(timestep,i)
j=subwrd(strings,i)
t=substr(titles,j,34)
    say 'Saving wind forecast day'i' image...'
    'set lat 5 20'
    'set lon 116 128'
    'set t 'ts''
*    'define w'h'mag=mag(u,v)'
    'setMap'
    'setColor_winds'
    'set z 4'
    'set strmden -6 0.5 0.1'
    'set gxout stream'
    'set cthick 4'
    'd u;v;mag(u,v)'
    'set line 14 1 5'
    'draw shp 'shpsrc'/world_shp/country.shp'
    'set string 1 c 5.5 0'
    'set strsiz 0.075'
    'draw string 4.25 0.8 WRF Ensemble Forecast Initialized at 'date2
    'set strsiz 0.15'
    'set string 1 tc 5.5 0'
    'draw string 4.25 10.9 Winds( 850mb | m/s)'
    'draw string 4.25 10.6 Valid from 't''
    'cbarn 1 1 7.5 6'
    'set string 1 c 5.5 0'
    'set strsiz 0.13'
    'draw string 7.5 7.85 [m/s]'
    'setLabel_MO'
    'draw string 2.33 1.79 observatory.ph'
    'gxprint 'outdir'/wrf-'h'hr_winds_'date'.png'
i=i+1
endwhile
*-------------------------------------------------------*
* PLOT RH MAPS
*-------------------------------------------------------*
hour = '24 48 72 96 120'
timestep = '25 49 73 97 121'
strings = '1 35 69 103 137'
titles = ''d1title''d2title''d3title''d4title''d5title''
i=1
k=0
while (i<=5)
h=subwrd(hour,i)
ts=subwrd(timestep,i)
j=subwrd(strings,i)
t=substr(titles,j,34)
    say 'Saving RH forecast day'i' image...'
    'set lat 5 20'
    'set lon 116 128'
    'set t 'ts''
    'setMap'
    'setColor_rh'
    'set z 1'
    'd rh2'
    'set line 75 1 5'
    'draw shp 'shpsrc'/world_shp/country.shp'
    'set string 1 c 5.5 0'
    'set strsiz 0.075'
    'draw string 4.25 0.8 WRF Ensemble Forecast Initialized at 'date2
    'set strsiz 0.15'
    'set string 1 tc 5.5 0'
    'draw string 4.25 10.9 Relative Humidity( 2m | % )'
    'draw string 4.25 10.6 Valid from 't''
    'cbarn 1 1 7.5 6'
    'set string 1 c 5.5 0'
    'set strsiz 0.13'
    'draw string 7.5 8.4 [%]'
    'setLabel_MO'
    'draw string 2.33 1.79 observatory.ph'
    'gxprint 'outdir'/wrf-'h'hr_rh_'date'.png'
k=k+1
i=i+1
endwhile
*-------------------------------------------------------*
* PLOT TEMPERATURE MAPS
*-------------------------------------------------------*
hour = '24 48 72 96 120'
timestep = '25 49 73 97 121'
strings = '1 35 69 103 137'
titles = ''d1title''d2title''d3title''d4title''d5title''
i=1
k=0
while (i<=5)
h=subwrd(hour,i)
ts=subwrd(timestep,i)
j=subwrd(strings,i)
t=substr(titles,j,34)
    say 'Saving temperature forecast day'i' image...'
    'set lat 5 20'
    'set lon 116 128'
    'set t 'ts''
    'setMap'
    'setColor_t2'
    'd tsk-273.15'
    'set gxout contour'
    'set clevs 28 29 30 31'
    'set ccolor 0'
    'set clopts 0 4 0.12'
    'set clab masked'
    'd (tsk-273.15)*masksst'
    'setColor_t2'
    'set z 1'
    'd (t2-273.15)*mask'
    'set line 1 1 5'
    'draw shp 'shpsrc'/world_shp/country.shp'
    'set string 1 c 5.5 0'
    'set strsiz 0.075'
    'draw string 4.25 0.8 WRF Ensemble Forecast Initialized at 'date2
    'set strsiz 0.15'
    'set string 1 tc 5.5 0'
    'draw string 4.25 10.9 Air (2m) and Sea Surface Temperature ( `3.`0C )'
    'draw string 4.25 10.6 Valid from 't''
    'cbarn 1 1 7.5 6'
    'set string 1 c 5.5 0'
    'set strsiz 0.13'
    'draw string 7.5 9.2 [`3.`0C]'
    'setLabel_MO'
    'draw string 2.33 1.79 observatory.ph'
    'gxprint 'outdir'/wrf-'h'hr_t2_'date'.png'
k=k+1
i=i+1
endwhile
*-------------------------------------------------------*
* EXTRACT RH AND T2 for HEAT INDEX 
*-------------------------------------------------------*
'set z 1'
'set t 1 121'
'define rh=rh2'
'set sdfwrite nc/wrf-rh_'date'.nc'
'sdfwrite rh'
'c'

'set t 1 121'
'define t=t2'
'set sdfwrite nc/wrf-t2_'date'.nc'
'sdfwrite t'
'c'

'quit'
