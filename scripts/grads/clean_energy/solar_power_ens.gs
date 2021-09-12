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
*assume air density is 1.275

'set z 1'
'set t 1 121'
'define ghi = (swddni*coszen) + swddif'
'define c1 = (ghi*0+1)*-3.75'
'define c2 = (1.14*(t2-273.15))'
'define c3 = 0.0175*ghi'
'define Tcell = c1+c2+c3'

'define Tref = (ghi*0+1)*25'
'Ncell = 0.12*((ghi*0+1)-0.0045*(Tcell-Tref)+0.1*log10(ghi))'
'PPV = ghi*Ncell'

'set t 1'
'define ppv24=sum(PPV,t=1,t=24)'
'define ppv48=sum(PPV,t=25,t=48)'
'define ppv72=sum(PPV,t=49,t=72)'
'define ppv96=sum(PPV,t=73,t=96)'
'define ppv120=sum(PPV,t=97,t=120)'

*adjust to number of solar panels in 1 hectare = 7200
*adjust to MW
'define spanel = 7200'
'define cf = 0.2'
'define ppv24h=ppv24*spanel/1000000'
'define ppv48h=ppv48*spanel/1000000'
'define ppv72h=ppv72*spanel/1000000'
'define ppv96h=ppv96*spanel/1000000'
'define ppv120h=ppv120*spanel/1000000'

*'define ppv24h=ppv24'
*'define ppv48h=ppv48'
*'define ppv72h=ppv72'

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

'set grid off'
'set gxout shaded'
'set lat 5 20'
'set lon 116 128'
'set xlint 5'
'set ylint 5'
'set xlopts 1 1 0.18'
'set ylopts 1 1 0.2'
'set grads off'
'set mpdraw off'
'set strsiz 0.075'
'set string 1 c 5.5 0'
'draw string 4.25 0.2 WRF Ensemble Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 24-Hr Total Solar Power Potential (MW)'
'draw string 4.25 10.6 Valid from 't''
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.55 7.1 [MW]'
'setColor_PVO.gs'
'd ppv'h'h*mask'
'draw shp 'shpsrc'/world_shp/country.shp'

'cbarn 1 1 7.6 5.1'

'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 0.7 3.25 1.1'
'set line 1'
'draw rec 1.4 0.7 3.25 1.1'
'set strsiz 0.15'
'draw string 1.5 0.89 observatory.ph'
'set rgb 98 178 34 34'
'define solarsum=asum(ppv'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd solarsum/1000'
val=subwrd(result,4)
solarsum1=val
rc = math_nint(solarsum1)
'd 'rc''
val=subwrd(result,4)
output1=val
'set string 98 c 5.5 0'
'set strsiz 0.45'
'draw string 4.25 10.0 Total:'output1'GW'

'define solarmax=amax(ppv'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd solarmax'
val=subwrd(result,4)
solarmax1=val
rc = math_nint(solarmax1)
'd 'rc''
val=subwrd(result,4)
output2=val

'define solarave=aave(ppv'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd solarave'
val=subwrd(result,4)
solarave1=val
rc = math_nint(solarave1)
'd 'rc''
val=subwrd(result,4)
output3=val
'set strsiz 0.16'
*'draw string 5.8 10.1 Max: 'output2' MW'
*'draw string 5.8 9.8 Ave: 'output3' MW'
'set strsiz 0.10'
'draw string 4.25 9.55 Value above for Philippine landmass only'
'gxprint 'outdir'/wrf-'h'hr_ppv_'date'.png'
'c'

i=i+1
endwhile
'quit'
