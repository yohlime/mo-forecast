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
'set grid off'
'set gxout shaded'
'set lat 5 20'
'set lon 116 128'
'set grads off'
'set mpdraw off'
'set parea 0.25 8.25 0.6 9.35'

'set z 1'
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
hour = '24 48 72 96 120'
strings = '1 35 69 103 137'
titles = ''d1title''d2title''d3title''d4title''d5title''
i=1
while (i<=5)
h=subwrd(hour,i)
j=subwrd(strings,i)
t=substr(titles,j,34)
'set grads off'
'set grid off'
'set gxout shaded'
'set lat 5 20'
'set lon 116 128'
'set xlint 5'
'set ylint 5'
'set xlopts 1 1 0.18'
'set ylopts 1 1 0.2'
'set strsiz 0.075'
'set string 1 c 5.5 0'
'draw string 4.25 0.2 WRF Ensemble Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 24-Hr Total Wind Power Potential (MW)'
'draw string 4.25 10.6 Valid from 't''
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.55 7.1 [MW]'
'setColor_WPD.gs'
'd wpd'h'h'
'draw shp 'shpsrc'/world_shp/country.shp'

'cbarn 1 1 7.6 5.1'

'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 0.7 3.25 1.1'
'set line 1'
'draw rec 1.4 0.7 3.25 1.1'
'set strsiz 0.15'
'draw string 1.5 0.89 observatory.ph'
'set rgb 98 0 0 205'
'define windsum=asum(wpd'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd windsum/1000'
val=subwrd(result,4)
windsum1=val
rc = math_nint(windsum1)
'd 'rc''
val=subwrd(result,4)
output1=val
'set string 98 c 5.5 0'
'set strsiz 0.45'
'draw string 4.25 10.0 Total:'output1'GW'

'define windmax=amax(wpd'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd windmax'
val=subwrd(result,4)
windmax1=val
rc = math_nint(windmax1)
'd 'rc''
val=subwrd(result,4)
output2=val

'define windave=aave(wpd'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd windave'
val=subwrd(result,4)
windave1=val
rc = math_nint(windave1)
'd 'rc''
val=subwrd(result,4)
output3=val
'set strsiz 0.16'
*'draw string 5.8 10.1 Max: 'output2' MW'
*'draw string 5.8 9.8 Ave: 'output3' MW'
'set strsiz 0.10'
'draw string 4.25 9.55 Value above for Philippine landmass only'
'gxprint 'outdir'/wrf-'h'hr_wpd_'date'.png'
'c'
i=i+1
endwhile


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
