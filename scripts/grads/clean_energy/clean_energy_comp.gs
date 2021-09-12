date='2021-09-11_08PHT'
d1title='2021-09-11_08 to 2021-09-12_08 PHT'
d2title='2021-09-12_08 to 2021-09-13_08 PHT'
d3title='2021-09-13_08 to 2021-09-14_08 PHT'
d4title='2021-09-14_08 to 2021-09-15_08 PHT'
d5title='2021-09-15_08 to 2021-09-16_08 PHT'
outdir='/home/modelman/forecast/scripts/timeseries/csv'
wrfres='5'
date2='2021-09-11_08 PHT'

'sdfopen /home/modelman/forecast/model/ENSEMBLE/wrffcst_d01_2021-09-11_00_ens.nc'

'sdfopen mask.nc'
'set dfile 2'
'set z 1'
'set t 1'
'define mask = z'
'close 2'
'set dfile 1'

***************** SOLAR POWER POTENTIAL ********************
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

***************** WIND POWER POTENTIAL ********************
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
* extract clean energy  daily values
**************************************
stn = 'PH'
hour = '24 48 72 96 120'
i=1
while (i <= 5)
h = subwrd(hour,i)

'define solarsum=asum(ppv'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd solarsum'
val=subwrd(result,4)
output=val
res=write(''outdir'/'date'_'stn'_SolarTotal.csv',output,append)

'define solarmax=amax(ppv'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd solarmax'
val=subwrd(result,4)
output=val
res=write(''outdir'/'date'_'stn'_SolarMax.csv',output,append)

'define solarave=aave(ppv'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd solarave'
val=subwrd(result,4)
output=val
res=write(''outdir'/'date'_'stn'_SolarAve.csv',output,append)

'define windsum=asum(wpd'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd windsum'
val=subwrd(result,4)
output=val
res=write(''outdir'/'date'_'stn'_WindTotal.csv',output,append)

'define windmax=amax(wpd'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd windmax'
val=subwrd(result,4)
output=val
res=write(''outdir'/'date'_'stn'_WindMax.csv',output,append)

'define windave=aave(wpd'h'h*mask, lon=116, lon=128, lat=5, lat=20)'
'd windave'
val=subwrd(result,4)
output=val
res=write(''outdir'/'date'_'stn'_WindAve.csv',output,append)

i=i+1
endwhile
'quit'
