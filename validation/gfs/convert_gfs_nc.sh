#!/bin/bash

#export VAL_DIR=$MAINDIR/validation/day1
GFS_INDIR=${GFSDIR}
GFS_VALDIR=${VAL_DIR}/gfs/nc/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}

NCL=/home/miniconda3/envs/ncl_stable/bin/ncl
mkdir -p $GFS_VALDIR

# Replace forward slash with escapes for sed to replace directory paths
GFS_INDIR2=${GFS_INDIR//\//\\/}
GFS_VALDIR2=${GFS_VALDIR//\//\\/}

VAR="pr"
HOUR="24"
# 24-hour period
for i in {000..024}
do
	FILE="GFS${i}"
	sed -i "5s/.*/   grib_in  = addfile(\"${GFS_INDIR2}\/${FILE}.grb\",\"r\")/" ${VAR}_convert.ncl
	sed -i "11s/.*/  ncdf_out = addfile(\"${GFS_VALDIR2}\/${FILE}_${VAR}.nc\",\"c\") ; create output netCDF file/" ${VAR}_convert.ncl
	$NCL pr_convert.ncl
	echo "${i} is done"
done

