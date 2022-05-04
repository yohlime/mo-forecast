#!/usr/bin/env bash

echo "------------------------------------------"
echo " Downloading latest assimilation files... "
echo "------------------------------------------"

# choose window hour (how many hours before or after the initialization time)
WH=${WINDOW_HOUR}
# choose which data type to download
DTYPE="point"
# choose which data sources to include
DSOURCE="acars HDW metar maritime raob"
# available: HDW HDW1 POES acars acarsProfiles maritime metar profiler radiometer raob sao satrad

mkdir -p "$TEMP_DIR"
for j in $DSOURCE; do
  mkdir -p "$MADISDIR/$j/netcdf"
done

# Set variables
DL_LIST=$TEMP_DIR/madis_dl_list.txt
DL_OUT=$TEMP_DIR/madis_dl.out
DL_LOG_FILE="$MAINDIR/input/madis_files/madis_dl_speed.log"

# get start and end of window hours
SDATE=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} ${FCST_ZZ}:00:00 $((WH)) hours ago" +'%Y-%m-%d %H:%M:%S')
EDATE=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} ${FCST_ZZ}:00:00 $((WH + 1)) hours" +'%Y-%m-%d %H:%M:%S')
TDATE=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} ${FCST_ZZ}:00:00 $((WH)) hours" +'%Y-%m-%d %H:%M:%S')
TH=${TDATE:11:2}

# URL
BASE_URL="https://madis-data.ncep.noaa.gov/madisPublic1/data/$DTYPE"

# Create download list
touch "$DL_LIST"

CDATE=$SDATE
while [ "$CDATE" != "$EDATE" ]; do
  for j in $DSOURCE; do
    #echo data ${j}
    #echo CDATE "$CDATE"
    YY2=${CDATE:0:4}
    MM2=${CDATE:5:2}
    DD2=${CDATE:8:2}
    HH2=${CDATE:11:2}
    #echo hour $HH2
    DIR_SOURCE="$j/netcdf"
    FILE_NAME="${YY2}${MM2}${DD2}_${HH2}00.gz"
    URL="$BASE_URL/$DIR_SOURCE/$FILE_NAME"
    echo "$URL" >>"$DL_LIST"
    echo -e "\tdir=$MADISDIR/$j/netcdf" >>"$DL_LIST"
  done
  CDATE=$(date -d "$CDATE 1 hour" +'%Y-%m-%d %H:%M:%S')
  #echo CDATE NEW "$CDATE"
done

# Wait for files to be available

# Exit if file still doesn't exist

DATE_STR=$(date +"%Y%m%d,%H")
# Record start time
DL_STIME=$(date +%s)

# Download
DL_LOG="$MAINDIR/input/madis_files/madis_dload_${FCST_YYYYMMDD}${FCST_ZZ}.log"
aria2c -j5 -x8 -i "$DL_LIST" -l "$DL_LOG" --log-level=notice

# Record end time
DL_ETIME=$(date +%s)
# Compute elapsed time in seconds
DL_DURATION=$((DL_ETIME - DL_STIME))
# Get total download size
TOT_SIZE=$(du -sk "$MADISDIR/" | cut -f1)
# Compute download speed
DL_SPEED=$(bc <<<"scale=2; ${TOT_SIZE}/${DL_DURATION}")
# Log Speed
echo "${DATE_STR},${DL_DURATION},${TOT_SIZE},${DL_SPEED}" >>"$DL_LOG_FILE"

# Cleanup
rm -f "$DL_LIST"
rm -f "$DL_OUT"

# Unzip
for j in $DSOURCE; do
  cd "$MADISDIR/$j/netcdf" || continue
  gzip -d ./*.gz
done

echo "------------------------------------------"
echo " Finished downloading assimilation files! "
echo "------------------------------------------"
