date='2021-06-20_20PHT'
d1title='2021-06-20_20 to 2021-06-21_20 PHT'
d2title='2021-06-21_20 to 2021-06-22_20 PHT'
d3title='2021-06-22_20 to 2021-06-23_20 PHT'
d4title='2021-06-23_20 to 2021-06-24_20 PHT'
d5title='2021-06-24_20 to 2021-06-25_20 PHT'
outdir='/home/modelman/forecast/output/maps'
wrfres='5'
date2='2021-06-20_20 PHT'

'open /home/modelman/forecast/model/ARWpost/mowcr_solar/wrffcst_d01_2021-06-20_12.ctl'

shpsrc='/home/modelman/forecast/scripts/shp'

'set mpdset hires'
'set display color white'
'c'
'set grid off'
'set gxout shaded'
'set lat 5 20'
'set lon 116 128'
'set grads off'
'set mpdraw off'
'set parea 0.25 8.25 1.5 10.25'

'set z 4'
'set t 1 121'
'define windpow=pow(wspd(z=1),3)'
'define a = 0.5'
* constant
'define p = 1.23'
* air density
'define r = 52'
* blade length of turbine (radius)
'define cp = 0.4'
* power coefficient
'define cf = 0.4'
* cf = capacity factor (40%)
'define turb = 4'
* assume 4 wind turbines in one hectare
'define swarea = 8495'
*swept area of turbine

*Wind power density equation
'define wpd = turb*(a*p*swarea*cp*windpow)'
'set t 1'
'define wpd24=sum(wpd,t=1,t=24)'
'define wpd48=sum(wpd,t=25,t=48)'
'define wpd72=sum(wpd,t=49,t=72)'
'define wpd96=sum(wpd,t=73,t=96)'
'define wpd120=sum(wpd,t=97,t=120)'

*convert to MW
'define wpd24h=wpd24/1000000'
'define wpd48h=wpd48/1000000'
'define wpd72h=wpd72/1000000'
'define wpd96h=wpd96/1000000'
'define wpd120h=wpd120/1000000'

**************************************
*Plot 24 hours
**************************************
'set strsiz 0.075'
'set string 1 tl 5.5 0'
'draw string 4 0.8 WRF Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 `n24-Hr Total Wind Power Potential (MW)'
'draw string 4.25 10.6 Valid from 'd1title''
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.55 8.0 `n[MW]'
'setColor_WPD.gs'
'd wpd24h'
'draw shp 'shpsrc'/world_shp/country.shp'

'cbarn 1 1 7.5 6'

'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 1.5 1.79 observatory.ph'
'gxprint 'outdir'/wrf-24hr_wpd_'date'.png'
'c'

**************************************
*Plot 48 hours
**************************************
'set grads off'
'set strsiz 0.075'
'set string 1 tl 5.5 0'
'draw string 4 0.8 WRF Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 `n24-Hr Total Wind Power Potential (MW)'
'draw string 4.25 10.6 Valid from 'd2title''
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.55 8.0 [MW]'
'setColor_WPD.gs'
'd wpd48h'
'cbarn 1 1 7.5 6'
'draw shp 'shpsrc'/world_shp/country.shp'

'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 1.5 1.79 observatory.ph'
'gxprint 'outdir'/wrf-48hr_wpd_'date'.png'
'c'

**************************************
*Plot 72 hours
**************************************
'set grads off'
'set strsiz 0.075'
'set string 1 tl 5.5 0'
'draw string 4 0.8 WRF Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 `n24-Hr Total Wind Power Potential (MW)'
'draw string 4.25 10.6 Valid from 'd3title''
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.55 8.0 `n[MW]'
'setColor_WPD.gs'
'd wpd72h'
'cbarn 1 1 7.5 6'
'draw shp 'shpsrc'/world_shp/country.shp'

'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 1.5 1.79 observatory.ph'
'gxprint 'outdir'/wrf-72hr_wpd_'date'.png'
'c'

**************************************
*Plot 96 hours
**************************************
'set grads off'
'set strsiz 0.075'
'set string 1 tl 5.5 0'
'draw string 4 0.8 WRF Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 `n24-Hr Total Wind Power Potential (MW)'
'draw string 4.25 10.6 Valid from 'd4title''
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.55 8.0 `n[MW]'
'setColor_WPD.gs'
'd wpd96h'
'cbarn 1 1 7.5 6'
'draw shp 'shpsrc'/world_shp/country.shp'

'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 1.5 1.79 observatory.ph'
'gxprint 'outdir'/wrf-96hr_wpd_'date'.png'
'c'

**************************************
*Plot 120 hours
**************************************
'set grads off'
'set strsiz 0.075'
'set string 1 tl 5.5 0'
'draw string 4 0.8 WRF Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 `n24-Hr Total Wind Power Potential (MW)'
'draw string 4.25 10.6 Valid from 'd5title''
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.55 8.0 `n[MW]'
'setColor_WPD.gs'
'd wpd120h'
'cbarn 1 1 7.5 6'
'draw shp 'shpsrc'/world_shp/country.shp'

'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 1.5 1.79 observatory.ph'
'gxprint 'outdir'/wrf-120hr_wpd_'date'.png'
'c'

************************
* extract wind speed over Pililla all eta levels
*********************
h =1
while (h<=34)
'set z 'h''
val2 = subwrd(result,2)
'set t 1'
* Pililla
'set lat 14.4722'
'set lon 121.3491'
'd wspd'
 val= subwrd(result,4)
  output=val
 res=write(''outdir'/../sounding/sounding_Pililla_'date'.csv',h' 'output,append)
h=h+1
endwhile
'quit'
