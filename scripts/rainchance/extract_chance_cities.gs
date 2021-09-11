date='2021-09-07_20PHT'
date2='2021-09-07_20 PHT'
indir='/home/modelman/forecast/scripts/rainchance/nc'
outdir='/home/modelman/forecast/scripts/rainchance/csv'

ifile = cities.txt
******for extracting the data*******************
res = read(ifile)
stat=sublin(res,1)
line=sublin(res,2)
while(stat=0)
  stn=subwrd(line,1)
  lat=subwrd(line,2)
  lon=subwrd(line,3)

day = 1
while (day<=5)
'sdfopen 'indir'/rainchance_day'day'_'date'.nc'

'set lat 'lat
'set lon 'lon
'd chance'
val=subwrd(result,4)
output=val
res=write(''outdir'/'date'_'stn'_chance.csv',output,append)

day = day + 1
endwhile

res = read(ifile)
stat=sublin(res,1)
line=sublin(res,2)
endwhile
'reinit'
close(ifile)

'quit'
