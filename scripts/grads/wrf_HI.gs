date='2020-03-23_02PHT'
d1title='2020-03-23_02 to 2020-03-24_02 PHT'
d2title='2020-03-24_02 to 2020-03-25_02 PHT'
d3title='2020-03-25_02 to 2020-03-26_02 PHT'
d4title='2020-03-26_02 to 2020-03-27_02 PHT'
d5title='2020-03-27_02 to 2020-03-28_02 PHT'
outdir='/home/modelman/forecast/output/maps'
wrfres='5'
date2='2020-03-23_02 PHT'

'sdfopen /home/modelman/forecast/scripts/grads/nc/wrf-HI_2020-03-23_02PHT.nc'

shpsrc='/home/modelman/forecast/scripts/shp'

'sdfopen mask.nc'
'set dfile 2'
'set z 1'
'set t 1'
'define mask = z'
'close 2'
'set dfile 1'
'set z 1'
'set mpdset hires'
'set display color white'
'c'
'set parea 0.25 8.25 1.5 10.25'
'set grid off'
'set gxout shaded'
'set lat 5 20'
'set lon 116 128'

*** plot 24hr acc precip
say Processing 24hr forecast...
'set t 25'
say Saving 24hr forecast image...
'c'
'set grads off'
'set mpdraw off'
'set gxout shaded'
'setColor_hi'
'set z 1'
'd hi*mask'

'set string 1 c 5.5 0'
'set strsiz 0.075'
'draw string 5.5 0.8 WRF Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 Heat Index( `3.`0C )'
'draw string 4.25 10.6 Valid from 'd1title''
'cbarn 1 1 7.5 6'
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.5 7.45 [`3.`0C]'
*'basemap O 0 0 M'
'set line 1 1 3'
'draw shp 'shpsrc'/world_shp/country.shp'

'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 2.33 1.79 observatory.ph'
'gxprint 'outdir'/wrf-24hr_hi_'date'.png'
'c'

say Processing 48hr forecast...
'set t 49'
say Saving 48hr forecast image...
'c'
'set grads off'
'set mpdraw off'
'set gxout shaded'
'setColor_hi'
'set z 1'
'd hi*mask'

'set strsiz 0.075'
'draw string 5.5 0.8 WRF Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 Heat Index( `3.`0C )'
'draw string 4.25 10.6 Valid from 'd2title''
'cbarn 1 1 7.5 6'
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.5 7.45 [`3.`0C]'
*'basemap O 0 0 M'
'set line 1 1 3'
'draw shp 'shpsrc'/world_shp/country.shp'

'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 2.33 1.79 observatory.ph'
'gxprint 'outdir'/wrf-48hr_hi_'date'.png'
'c'

*** plot 72hr acc precip
say Processing 72hr forecast...
'set t 73'
*'define w72dir=u,v'
say Saving 72hr forecast image...
'c'

'set grads off'
'set mpdraw off'
'set gxout shaded'
'setColor_hi'
'set z 1'
'd hi*mask'

'set strsiz 0.075'
'draw string 5.5 0.8 WRF Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 Heat Index( `3.`0C )'
'draw string 4.25 10.6 Valid from 'd3title''
'cbarn 1 1 7.5 6'
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.5 7.45 [`3.`0C]'
*'basemap O 0 0 M'
'set line 1 1 3'
'draw shp 'shpsrc'/world_shp/country.shp'


'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 2.33 1.79 observatory.ph'
'gxprint 'outdir'/wrf-72hr_hi_'date'.png'
'c'

say Processing 96hr forecast...
'set t 97'
*'define w96dir=u,v'
say Saving 96hr forecast image...
'c'

'set grads off'
'set mpdraw off'
'set gxout shaded'
'setColor_hi'
'set z 1'
'd hi*mask'

'set strsiz 0.075'
'draw string 5.5 0.8 WRF Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 Heat Index( `3.`0C )'
'draw string 4.25 10.6 Valid from 'd4title''
'cbarn 1 1 7.5 6'
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.5 7.45 [`3.`0C]'
*'basemap O 0 0 M'
'set line 1 1 3'
'draw shp 'shpsrc'/world_shp/country.shp'


'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 2.33 1.79 observatory.ph'
'gxprint 'outdir'/wrf-96hr_hi_'date'.png'
'c'

say Processing 120hr forecast...
'set t 121'
*'define w120dir=u,v'
say Saving 120hr forecast image...
'c'

'set grads off'
'set mpdraw off'
'set gxout shaded'
'setColor_hi'
'set z 1'
'd hi*mask'

'set strsiz 0.075'
'draw string 5.5 0.8 WRF Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 Heat Index( `3.`0C )'
'draw string 4.25 10.6 Valid from 'd3title''
'cbarn 1 1 7.5 6'
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.5 7.45 [`3.`0C]'
*'basemap O 0 0 M'
'set line 1 1 3'
'draw shp 'shpsrc'/world_shp/country.shp'


'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 2.33 1.79 observatory.ph'
'gxprint 'outdir'/wrf-120hr_hi_'date'.png'
'c'

'quit'
