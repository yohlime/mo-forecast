date='2021-06-08_08PHT'
outdir='/home/modelman/forecast/output/hourly'
date2='2021-06-08_08 PHT'
'open /home/modelman/forecast/model/ARWpost/mowcr_D1/wrffcst_d01_2021-06-08_00.ctl'
shpsrc='/home/modelman/forecast/scripts/shp'
**Set up plotting resources

'set mpdset hires'
'set display color white'
'c'
'set grid off'
'set gxout shaded'
'set grads off'
'set mpdraw off'
'set parea 0.25 8.25 1.5 10.25'
'setColor_gsmap_hr'
'set lat 14.3 14.8'
'set lon 120.8 121.5'
'set z 1'

*Extacting lat lon max time part
*Ignore if not needed
*'q file'
*line=sublin(result,5)
*xmax=subwrd(line,3)
*ymax=subwrd(line,6)
*tmax=subwrd(line,12)

tt=1
tmax=72

while(tt <= tmax)


*get date strings
'set t 'tt
'query time'
datestr = subwrd (result, 3)
say datestr
hourp   = substr(datestr,1,2) + 8
dayp    = substr(datestr,4,2)
monthp  = substr(datestr,6,3)
yearp   = substr(datestr,9,4)

if(hourp > 24 & hourp <= 48)
hourp = hourp - 24
dayp = dayp + 1
endif

if(hourp > 48 & hourp <=72)
hourp = hourp - 48
dayp = dayp + 2
endif

if(hourp < 10)
hourp = '0'hourp
endif

*Required Grads functions for converting months
*Located at /opt/opengrads/Resources/Scripts

*'run atoi.gsf'
*'run chcase.gsf'
*'run itoa.gsf'
*'run rgnwrd.gsf'
*'run cmonth.gsf'

rc = gsfallow( 'on' )
monp = cmonth(monthp)
if(monp < 10)
monp = '0'monp
endif

*Get date strings

'set t 'tt+1
'query time'
datestro = subwrd (result, 3)
houro   = substr(datestro,1,2) + 8
dayo    = substr(datestro,4,2)
montho  = substr(datestro,6,3)
yearo   = substr(datestro,9,4)

rc = gsfallow( 'on' )
mono=cmonth(montho)
if(mono < 10)
mono = '0'mono
endif

*If the time steps are beyond 24 hrs, subtract 24
if(houro > 24 & houro <= 48)
houro = houro - 24
dayo = dayo + 1
endif

if(houro > 48 & houro <=72)
houro = houro - 48
dayo = dayo + 2
endif

*if(dayo < 10)
*dayo = '0'dayo
*endif
*If hour is less than 10, add a placeholder before the number
if(houro < 10)
houro = '0'houro
endif


*Plot the variable
'set grads off'
'setColor_gsmap_hr'
'define rsum=(rainc(t='tt+1')+rainnc(t='tt+1'))-(rainc(t='tt')+rainnc(t='tt'))'
'd rsum'

*Draw shapefile
'draw shp 'shpsrc'/phil/provinces/provinces.shp'

**Draw Title color bar and unit
'cbarn 1 1 7.5 6'
'set string 1 c 5.5 0'
'set strsiz 0.13'
'draw string 7.7 8.85 [mm/hr]'

'set rgb 99 255 255 255 200'
'set line 99 1'
'draw recf 1.4 1.6 3.25 2'
'set line 1'
'draw rec 1.4 1.6 3.25 2'
'set strsiz 0.15'
'draw string 2.33 1.79 observatory.ph'

'set strsiz 0.075'
'set string 1 tl 5.5 0'
'draw string 4 0.8 WRF Forecast Initialized at 'date2
'set strsiz 0.15'
'set string 1 tc 5.5 0'
'draw string 4.25 10.9 Hourly Rainfall(mm/hr)'
'draw string 4.25 10.6 Valid from 'yearp'-'monp'-'dayp'_'hourp' to 'yearo'-'mono'-'dayo'_'houro' PHT'


**Print
if (tt < 25)
'gxprint 'outdir'/first24/mnl_hourly_rainfall_'yearp'-'monp'-'dayp'_'hourp'PHT.png'
else
'gxprint 'outdir'/mnl_hourly_rainfall_'yearp'-'monp'-'dayp'_'hourp'PHT.png'
endif

*'gxprint test/hourly_rainfall_'yearp'-'monp'-'dayp':'hourp'PhT.png'
'c'
tt=tt+1
endwhile

'quit'


