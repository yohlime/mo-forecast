#!/usr/bin/env bash

########## Dynamic Variables ##########
# Get date in UTC minus offset
OFFSET=6
if [ -z "$FCST_YYYYMMDD" ]; then
    FCST_YYYYMMDD=$(date -d "$OFFSET hours ago" -u +"%Y%m%d")
    export FCST_YYYYMMDD
fi
if [ -z "$FCST_ZZ" ]; then
    FCST_ZZ=$(date -d "$OFFSET hours ago" -u +"%H")
    export FCST_ZZ
fi
export FCST_YY=${FCST_YYYYMMDD:0:4}
export FCST_MM=${FCST_YYYYMMDD:4:2}
export FCST_DD=${FCST_YYYYMMDD:6:2}

# Get end date
FCST_YYYYMMDD2=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 ${WRF_FCST_DAYS} days" +'%Y%m%d')
FCST_ZZ2=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 ${WRF_FCST_DAYS} days" +'%H')
export FCST_YYYYMMDD2
export FCST_ZZ2
export FCST_YY2=${FCST_YYYYMMDD2:0:4}
export FCST_MM2=${FCST_YYYYMMDD2:4:2}
export FCST_DD2=${FCST_YYYYMMDD2:6:2}

export GFS_DIR="${GFS_BASE_DIR}/$FCST_YYYYMMDD/$FCST_ZZ"
export MADIS_DIR="${MADIS_BASE_DIR}/$FCST_YYYYMMDD/$FCST_ZZ"

# set variables for download_gsmap.sh
FCST_YYYYMMDD_GSMAP=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 12 hours ago" +'%Y%m%d')
export FCST_YYYYMMDD_GSMAP
FCST_ZZ_GSMAP=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 12 hours ago" +'%H')
export FCST_ZZ_GSMAP
export FCST_YY_GSMAP=${FCST_YYYYMMDD_GSMAP:0:4}
export FCST_MM_GSMAP=${FCST_YYYYMMDD_GSMAP:4:2}
export FCST_DD_GSMAP=${FCST_YYYYMMDD_GSMAP:6:2}
export GSMAP_TEMP_DIR="$TEMP_DIR/gsmap/$FCST_YYYYMMDD_GSMAP/$FCST_ZZ_GSMAP"

########## Dynamic Variables ##########
