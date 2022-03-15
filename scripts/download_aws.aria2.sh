#!/bin/bash
# aria2c -o stn_obs_24hr_2021-08-25_04.csv "https://panahon.observatory.ph/api/stations.php?24hr&type=csv" 
export ftp_proxy=http://proxy.admu.edu.ph:3128
export AWSDIR=$MAINDIR/input/aws_files

echo "------------------"
echo " Downloading latest AWS files... "
echo "------------------"

DATE_STR=$(date +"%Y%m%d,%H")

mkdir -p $TEMP_DIR
# Set variables
DL_LIST=$TEMP_DIR/aws_dl_list.txt
DL_OUT=$TEMP_DIR/aws_dl.out
DL_LOG_FILE="$AWSDIR/log/aws_dl_speed.log"

# get start date
SDATE=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} ${FCST_ZZ}:00:00 10 hours ago" +'%Y-%m-%d %H:%M:%S')


# URL Download AWS via website
NOW_DIR=https://panahon.observatory.ph/api/stations.php?24hr\&type=csv

# Create download list
touch ${DL_LIST}

CDATE=$SDATE
YY2=${CDATE:0:4}
MM2=${CDATE:5:2}
DD2=${CDATE:8:2}
HH2=${CDATE:11:2}
FILE_NAME="stn_obs_24hr_${YY2}-${MM2}-${DD2}_${HH2}PHT.csv"
URL="${NOW_DIR}"	
echo "${URL}" >> $DL_LIST
echo -e "\tdir=${AWSDIR}" >> $DL_LIST

# Wait for files to be available

# Exit if file still doesn't exist

# Record start time
DL_STIME=$(date +%s)

# Download
DL_LOG=${AWSDIR}/log/aws_dload_${FCST_YYYYMMDD}${FCST_ZZ}.log
#aria2c -i ${DL_LIST} -o ${FILE_NAME} -l ${DL_LOG}
aria2c -o ${FILE_NAME} ${URL} -l ${DL_LOG}

# Record end time
DL_ETIME=$(date +%s)
# Compute elapsed time in seconds
DL_DURATION=$(( ${$DL_ETIME} - ${$DL_STIME} ))
# Get total download size
TOT_SIZE=$(du -sk $AWSDIR | cut -f1)
# Compute download speed
DL_SPEED=$(bc <<< "scale=2; ${TOT_SIZE}/${DL_DURATION}")
# Log Speed
echo "${DATE_STR},${DL_DURATION},${TOT_SIZE},${DL_SPEED}" >> ${DL_LOG_FILE}

mv ${FILE_NAME} ${AWSDIR}
# Cleanup
rm -f "$DL_LIST"
rm -f "$DL_OUT"

echo "------------------"
echo " Finished downloading aws files! "
echo "------------------"