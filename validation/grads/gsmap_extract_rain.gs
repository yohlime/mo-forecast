date='2021-09-10_08PHT'
dfile='2021-09-10_00'
outdir='/home/modelman/forecast/output/validation/20210910/00'
gsmapdir='/home/modelman/forecast/validation/gsmap/nc'
data='gauge'
ifile = station.txt
*-------------------------------------------------------*
* EXTRACT GSMaP HOURLY RAINFALL
*-------------------------------------------------------*
'sdfopen 'gsmapdir'/gsmap_'data'_'dfile'_ph.nc'
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

    say 'Saving hourly GSMaP rainfall values...'
    i=1
    while (i<=24)
        'set t 'i''
        'set lat 'lat
        'set lon 'lon
        'd precip'
        val=subwrd(result,4)
        output=val
        res=write(''outdir'/gsmap_'date'_'stn'_pr.csv',output,append)
        i=i+1
    endwhile
    res = read(ifile)
    stat=sublin(res,1)
    line=sublin(res,2)
endwhile
close(ifile)
'quit'

