date='2021-09-10_08PHT'
outdir='/home/modelman/forecast/output/validation/20210910/00'
gfsdir='/home/modelman/forecast/validation/gfs/nc/20210910/00'
ifile = station.txt
*-------------------------------------------------------*
* EXTRACT GSMaP HOURLY RAINFALL
*-------------------------------------------------------*
res = read(ifile)
stat=sublin(res,1)
line=sublin(res,2)
while(stat=0)
    stn=subwrd(line,1)
    lat=subwrd(line,2)
    lon=subwrd(line,3)
    say 'Saving hourly GFS rainfall values...'

    i = 0
    while (i<=9)
        'sdfopen 'gfsdir'/GFS00'i'_pr.nc'
        'set lat 'lat
        'set lon 'lon
        'd pr*3600'
        val=subwrd(result,4)
        output=val
        res=write(''outdir'/gfs_'date'_'stn'_pr.csv',output,append)
        'reinit'
        i=i+1
    endwhile

    i =10
    while (i<=24)
        'sdfopen 'gfsdir'/GFS0'i'_pr.nc'
        'set lat 'lat
        'set lon 'lon
        'd pr*3600'
        val=subwrd(result,4)
        output=val
        res=write(''outdir'/gfs_'date'_'stn'_pr.csv',output,append)
        'reinit'
        i=i+1
    endwhile
    res = read(ifile)
    stat=sublin(res,1)
    line=sublin(res,2)
endwhile
close(ifile)
'quit'

