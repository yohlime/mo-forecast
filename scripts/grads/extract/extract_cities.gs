date='2021-09-11_08PHT'
'sdfopen /home/modelman/forecast/model/ENSEMBLE/wrffcst_d01_2021-09-11_00_ens.nc'
outdir='/home/modelman/forecast/scripts/timeseries/csv'


ifile = cities.txt
******for extracting the data*******************
'q file'
line=sublin(result,5)
xmax=subwrd(line,3)
ymax=subwrd(line,6)
tmax=subwrd(line,12)

res = read(ifile)
stat=sublin(res,1)
line=sublin(res,2)
while(stat=0)
  stn=subwrd(line,1)
  lat=subwrd(line,2)
  lon=subwrd(line,3)
  'set lat 'lat
  'set lon 'lon
  'set t 1 'tmax
'fprintf.gs rh2 'outdir'/'date'_'stn'_rh.csv %g 0'

  'set t 1 'tmax
'fprintf.gs t2 'outdir'/'date'_'stn'_t2.csv %g 0'

  'set t 1 'tmax
'fprintf.gs psfc 'outdir'/'date'_'stn'_psfc.csv %g 0'

  'set t 1 'tmax
'fprintf.gs ws10 'outdir'/'date'_'stn'_ws10.csv %g 0'

  'set t 1 'tmax
'fprintf.gs wd10 'outdir'/'date'_'stn'_wd10.csv %g 0'

  'set t 1 'tmax
'fprintf.gs u10m 'outdir'/'date'_'stn'_u10m.csv %g 0'

  'set t 1 'tmax
'fprintf.gs v10m 'outdir'/'date'_'stn'_v10m.csv %g 0'

  'set t 1 'tmax
'define ghi = (swddni*coszen) + swddif'
'fprintf.gs ghi 'outdir'/'date'_'stn'_ghi.csv %g 0'

  'set t 1 'tmax
'define windpow=pow(wspd(z=1),3)'
'fprintf.gs windpow 'outdir'/'date'_'stn'_windpow.csv %g 0'

'reinit'
'sdfopen /home/modelman/forecast/model/ENSEMBLE/wrffcst_d01_2021-09-11_00_ens.nc'

'set t 1'
'set z 1'
Tmin = 1
Tmax = 121
while(Tmin<=Tmax)

Tnext = Tmin + 1
'set lat 'lat
'set lon 'lon
'define rain=(rainc(t='Tnext')+rainnc(t='Tnext'))-(rainc(t='Tmin')+rainnc(t='Tmin'))'
'd rain'
val=subwrd(result,4)
output=val
res=write(''outdir'/'date'_'stn'_rain.csv',output,append)

Tmin = Tmin +1
endwhile

res = read(ifile)
  stat=sublin(res,1)
  line=sublin(res,2)

endwhile
'reinit'
close(ifile)


'quit'
