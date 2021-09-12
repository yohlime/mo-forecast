date='2021-09-11_08PHT'
d1title='2021-09-11_08 to 2021-09-12_08 PHT'
d2title='2021-09-12_08 to 2021-09-13_08 PHT'
d3title='2021-08-21_08 to 2021-08-22_08 PHT'
d4title='2021-09-14_08 to 2021-09-15_08 PHT'
d5title='2021-09-15_08 to 2021-09-16_08 PHT'
outdir='/home/modelman/forecast/output/climatology/20210911/00'
wrfres='5'
date2='2021-09-11_08 PHT'

'sdfopen /home/modelman/forecast/model/ENSEMBLE/wrffcst_d01_2021-09-11_00_ens.nc'

shpsrc='/home/modelman/forecast/scripts/shp'
climdir='/home/modelman/forecast/climatology'
month='09'

types = 'aphro trmm'
files = 'aphro_1951-2015 trmm_1998-2015'
labels = 'APHRODITE_V1101_1951-2015 TRMM_3B43_1998-2015'
tytitles = 'APHRODITE TRMM'

*-------------------------------------------------------*
* GET APHRODITE AND TRMM FILES 
*-------------------------------------------------------*
'set rgb 75 75 75 75'
ty=1
while (ty<=2)
type=subwrd(types,ty)
file=subwrd(files,ty)
label=subwrd(labels,ty)
title=subwrd(tytitles,ty)

* Monthly average of 1-Day Rain 
'sdfopen 'climdir'/'type'/'file'_ymonmean.nc'
'set dfile 2'
'set z 1'
'set t 'month''
'set lat 5 20'
'set lon 116 128'
'define obs = re(precip,0.05,0.05)'
'close 2'
'set dfile 1'

* Monthly 99th percentile of 1-Day Rain
'sdfopen 'climdir'/'type'/'file'_99pctl_'month'.nc'
'set dfile 2'
'set t 1'
'set lat 5 20'
'set lon 116 128'
'define obs99 = re(precip,0.05,0.05)'
'close 2'
'set dfile 1'

*-------------------------------------------------------*
* PLOT RAINFALL DIFFERENCE w/ MEAN MAPS
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
    say 'Saving 24hr rain difference forecast day'i' image...'
    'set lat 5 20'
    'set lon 116 128'
    'set t 'ts''
    'define p'h'=re(rainc+rainnc,0.05,0.05)'
    'setMap'
    'setColor_bias'
    if (i=1)
    'd p'h' - obs'
    else
    prevts=subwrd(hour,k)
    'd (p'h' - p'prevts') - obs'
    endif
    'set line 1 1 5'
    'draw shp 'shpsrc'/world_shp/country.shp'
    'set string 1 c 5.5 0'
    'set strsiz 0.075'
    'draw string 4.25 0.8 WRF Ensemble Forecast Initialized at 'date2''
    'draw string 4.25 0.6 'label' 1-Day 'month' Mean'
    'set strsiz 0.15'
    'set string 1 tc 5.5 0'
    'draw string 4.25 10.9 WRF-'title' Monthly Mean 24-Hr Total Rain (mm)'
    'draw string 4.25 10.6 From 't''
    'cbarn 1 1 7.5 6'
    'set string 1 c 5.5 0'
    'set strsiz 0.13'
    'draw string 7.5 9.15 [mm]'
    'setLabel_MO'
    'draw string 2.33 1.79 observatory.ph'
    'gxprint 'outdir'/wrf-'h'hr_rain_d'i'-'type'mm_'date'.png'
k=k+1
i=i+1
endwhile
*-------------------------------------------------------*
* PLOT RAINFALL DIFFERENCE w/ 99th PCTL MAPS
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
    say 'Saving 24hr rain difference 99th PCTL forecast day'i' image...'
    'set lat 5 20'
    'set lon 116 128'
    'set t 'ts''
    'define p'h'=re(rainc+rainnc,0.05,0.05)'
    'setMap'
    'setColor_bias'
    if (i=1)
    'd p'h' - obs99'
    else
    prevts=subwrd(hour,k)
    'd (p'h' - p'prevts') - obs99'
    endif
    'set line 1 1 5'
    'draw shp 'shpsrc'/world_shp/country.shp'
    'set string 1 c 5.5 0'
    'set strsiz 0.075'
    'draw string 4.25 0.8 WRF Ensemble Forecast Initialized at 'date2''
    'draw string 4.25 0.6 'label' 1-Day 'month' 99th %ile'
    'set strsiz 0.15'
    'set string 1 tc 5.5 0'
    'draw string 4.25 10.9 WRF-'title' Monthly 99th PCTL 24-Hr Total Rain (mm)'
    'draw string 4.25 10.6 From 't''
    'cbarn 1 1 7.5 6'
    'set string 1 c 5.5 0'
    'set strsiz 0.13'
    'draw string 7.5 9.15 [mm]'
    'setLabel_MO'
    'draw string 2.33 1.79 observatory.ph'
    'gxprint 'outdir'/wrf-'h'hr_rain_d'i'-'type'99_'date'.png'
k=k+1
i=i+1
endwhile

ty=ty+1
endwhile
'quit'
