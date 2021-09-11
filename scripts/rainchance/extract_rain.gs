date='2021-09-07_20PHT'
date2='2021-09-07_20 PHT'
wrfrun='wrffcst_d01_2021-09-07_12'
indir='/home/modelman/forecast/model/ENSEMBLE'
outdir='/home/modelman/forecast/model/ENSEMBLE'

run = 1
while (run <= 3)

'sdfopen 'indir'/mowcr_solar_run'run'/'wrfrun'.nc'

'set mpdset hires'
'set display color white'
'c'
'set grid off'
'set gxout shaded'
'set lat 5 20'
'set lon 116 128'

*** plot 24hr acc precip
say Processing 24hr forecast...
'set t 25'
'set z 1'
'define p24=rainc+rainnc'
'set sdfwrite 'outdir'/mowcr_solar_run'run'/wrf-day1_'date'.nc'
'sdfwrite p24'
'c'
'set t 49'
'define p48=rainc+rainnc'
'set sdfwrite 'outdir'/mowcr_solar_run'run'/wrf-day2_'date'.nc'
'sdfwrite p48'
'c'
'set t 73'
'define p72=rainc+rainnc'
'set sdfwrite 'outdir'/mowcr_solar_run'run'/wrf-day3_'date'.nc'
'sdfwrite p72'
'c'
'set t 97'
'define p96=rainc+rainnc'
'set sdfwrite 'outdir'/mowcr_solar_run'run'/wrf-day4_'date'.nc'
'sdfwrite p96'
'c'
'set t 121'
'define p120=rainc+rainnc'
'set sdfwrite 'outdir'/mowcr_solar_run'run'/wrf-day5_'date'.nc'
'sdfwrite p120'
'c'

run=run+1
endwhile
'quit'

