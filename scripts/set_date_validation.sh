########## Dynamic Variables ##########
# Get date in UTC minus offset (cron at 12:45 PHT the next day)
OFFSET=28 
[ -z "$FCST_YYYYMMDD" ] && export FCST_YYYYMMDD=$(date -d "$OFFSET hours ago" -u +"%Y%m%d")
[ -z "$FCST_ZZ" ] && export FCST_ZZ=$(date -d "$OFFSET hours ago" -u +"%H")
export FCST_YY=${FCST_YYYYMMDD:0:4}
export FCST_MM=${FCST_YYYYMMDD:4:2}
export FCST_DD=${FCST_YYYYMMDD:6:2}

# Get end date
export FCST_YYYYMMDD2=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 ${WRF_FCST_DAYS} days" +'%Y%m%d')
export FCST_ZZ2=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 ${WRF_FCST_DAYS} days" +'%H')
export FCST_YY2=${FCST_YYYYMMDD2:0:4}
export FCST_MM2=${FCST_YYYYMMDD2:4:2}
export FCST_DD2=${FCST_YYYYMMDD2:6:2}

export GFSDIR=$MAINDIR/input/gfs_files/$FCST_YYYYMMDD/$FCST_ZZ
export NUM_FILES=$(($WRF_FCST_DAYS*24+1))
########## Dynamic Variables ##########