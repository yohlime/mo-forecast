# Test data

## wrfout_d01_subset
Subset of a wrfout file. Contains variables required so `helpers.wrfpost.create_hour_ds()` will not throw an Error. Produced using `helpers.wrf.create_wrfout_subset()`.netcdf wrfout_d01_2023-09-01_subset

```
dimensions:
	Time = UNLIMITED ; // (25 currently)
	DateStrLen = 19 ;
	south_north = 415 ;
	west_east = 320 ;
	bottom_top = 10 ;
	bottom_top_stag = 11 ;
	west_east_stag = 321 ;
	south_north_stag = 416 ;
variables:
	char Times(Time, DateStrLen) ;
	float RAINC(Time, south_north, west_east) ;
	float RAINNC(Time, south_north, west_east) ;
	float T2(Time, south_north, west_east) ;
	float TSK(Time, south_north, west_east) ;
	float PSFC(Time, south_north, west_east) ;
	float Q2(Time, south_north, west_east) ;
	float HGT(Time, south_north, west_east) ;
	float P(Time, bottom_top, south_north, west_east) ;
	float PH(Time, bottom_top_stag, south_north, west_east) ;
	float PB(Time, bottom_top, south_north, west_east) ;
	float PHB(Time, bottom_top_stag, south_north, west_east) ;
	float U(Time, bottom_top, south_north, west_east_stag) ;
	float V(Time, bottom_top, south_north_stag, west_east) ;
	float SWDDNI(Time, south_north, west_east) ;
	float COSZEN(Time, south_north, west_east) ;
	float SWDDIF(Time, south_north, west_east) ;
	float XLAT(Time, south_north, west_east) ;
	float XLONG(Time, south_north, west_east) ;
	float XTIME(Time) ;
	float XLAT_U(Time, south_north, west_east_stag) ;
	float XLONG_U(Time, south_north, west_east_stag) ;
	float XLAT_V(Time, south_north_stag, west_east) ;
	float XLONG_V(Time, south_north_stag, west_east) ;
```