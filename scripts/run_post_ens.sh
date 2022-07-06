#!/bin/bash

source $SCRIPT_DIR/set_env_wrf.run.sh
PYTHONCONDA=/home/miniconda3/envs/toolbox/bin/python
ARW_OUT_FILE="wrffcst_d01_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}"
DATE_STR1=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00" +'%Y-%b-%d_%H')
read FCST_YY_Z FCST_MM_Z FCST_DD_Z FCST_HH_Z <<< ${DATE_STR1//[-_]/ }

echo "--------------------------"
echo " Making ensemble files... "
echo "--------------------------"

# -------------------------------------------- #
#              Ensemble                        #
# -------------------------------------------- #
cd ${WRF_ENS}

sed -i "1s/.*/dset \^${ARW_OUT_FILE}.dat/" wrffcst_d01.ctl
echo "test"
sed -i "743s/.*/tdef  121 linear ${FCST_ZZ}Z${FCST_DD}${FCST_MM_Z}${FCST_YY}      60MN/" wrffcst_d01.ctl
echo "endtest"

run_idx=1
cdo_ensfiles=""
while IFS=':' read -ra RUN_NAMES; do
  for run_name in "${RUN_NAMES[@]}"; do
    mkdir -p $run_name
    ln -s ${WRF_POSTDIR}/${run_name}/${ARW_OUT_FILE}.dat ${WRF_ENS}/${run_name}/.

    cp wrffcst_d01.ctl ${run_name}/${ARW_OUT_FILE}.ctl

    $CDO -f nc import_binary ${WRF_ENS}/${run_name}/${ARW_OUT_FILE}.ctl ${WRF_ENS}/${run_name}/${ARW_OUT_FILE}.nc
    cdo_ensfiles="$cdo_ensfiles ${WRF_ENS}/${run_name}/${ARW_OUT_FILE}.nc"
    run_idx=$((run_idx+1))
  done
done <<< "$WRF_RUN_NAMES"

$CDO ensmean $cdo_ensfiles ${WRF_ENS}/${ARW_OUT_FILE}_ens.nc

# -------------------------------------------- #
#              Postprocessing                  #
# -------------------------------------------- #
cd ${MAINDIR}/scripts/grads

DATE_STR1=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 8 hours" +'%Y-%m-%d_%H')
read FCST_YY_PHT FCST_MM_PHT FCST_DD_PHT FCST_HH_PHT <<< ${DATE_STR1//[-_]/ }

DATE_STRM=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 8 hours" +'%Y-%B-%d_%H')
read FCST_YY_PHT2 FCST_MM_PHT2 FCST_DD_PHT2 FCST_HH_PHT2 <<< ${DATE_STR1//[-_]/ }

sed -i "1s/.*/date='${DATE_STR1}PHT'/" wrf_clim.gs
sed -i "9s/.*/date2='${DATE_STR1} PHT'/" wrf_clim.gs
DATE_STR2=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 32 hours" +'%Y-%m-%d_%H')
sed -i "2s/.*/d1title='${DATE_STR1} to ${DATE_STR2} PHT'/" wrf_clim.gs
DATE_STR3=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 56 hours" +'%Y-%m-%d_%H')
sed -i "3s/.*/d2title='${DATE_STR2} to ${DATE_STR3} PHT'/" wrf_clim.gs
DATE_STR4=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 80 hours" +'%Y-%m-%d_%H')
sed -i "4s/.*/d3title='${DATE_STR3} to ${DATE_STR4} PHT'/" wrf_clim.gs
DATE_STR5=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 104 hours" +'%Y-%m-%d_%H')
sed -i "5s/.*/d4title='${DATE_STR4} to ${DATE_STR5} PHT'/" wrf_clim.gs
DATE_STR6=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 128 hours" +'%Y-%m-%d_%H')
sed -i "6s/.*/d5title='${DATE_STR5} to ${DATE_STR6} PHT'/" wrf_clim.gs


sed -i "7s~.*~outdir='${OUTDIR}/climatology/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}'~" wrf_clim.gs
sed -i "11s~.*~'sdfopen ${WRF_ENS}/${ARW_OUT_FILE}_ens.nc'~" wrf_clim.gs
sed -i "14s~.*~climdir='${MAINDIR}/climatology/frJulie/01_forForecasting'~" wrf_clim.gs
sed -i "15s~.*~month='${FCST_MM_PHT}'~" wrf_clim.gs
sed -i "16s~.*~monname='${FCST_MM_PHT2}'~" wrf_clim.gs

# compare with climatology
mkdir -p ${OUTDIR}/climatology/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}
grads -pbc wrf_clim.gs

echo "------------------"
echo " Finished postprocessing! "
echo "------------------"

# --------------------------------------- #
#    Delete current ensemble files        #
# --------------------------------------- #

rm -f ${WRF_ENS}/${WRF_NAMELIST_SUFF1}/${ARW_OUT_FILE}.*
rm -f ${WRF_ENS}/${WRF_NAMELIST_SUFF2}/${ARW_OUT_FILE}.*
rm -f ${WRF_ENS}/${WRF_NAMELIST_SUFF3}/${ARW_OUT_FILE}.*
rm -f ${WRF_ENS}/${WRF_NAMELIST_SUFF1}/wrf-day*_${DATE_STR1}PHT.nc
rm -f ${WRF_ENS}/${WRF_NAMELIST_SUFF2}/wrf-day*_${DATE_STR1}PHT.nc
rm -f ${WRF_ENS}/${WRF_NAMELIST_SUFF3}/wrf-day*_${DATE_STR1}PHT.nc

# ------------------------------- #
#        Delete past files        #
# ------------------------------- #

# Remove files from 1 month ago
DATE_STRR=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 1 month ago" +'%Y-%m-%d_%H')
read FCST_YY_R FCST_MM_R FCST_DD_R FCST_HH_R <<< ${DATE_STRR//[-_]/ }
MONTH_AGO="${FCST_YY_R}-${FCST_MM_R}-${FCST_DD_R}_${FCST_HH_R}"

echo " Removing files from ${MONTH_AGO} (1 month ago): "
echo " gfs_dload_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}.log "
# GFS log file
rm -f $MAINDIR/input/gfs_files/gfs_dload_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}.log

echo " wps_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}.out "
# WPS log file
rm -f ${WRF_MAINDIR}/WPS/wps_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}.out

# Remove files from 1 week ago
DATE_STRR=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 1 week ago" +'%Y-%m-%d_%H')
read FCST_YY_R FCST_MM_R FCST_DD_R FCST_HH_R <<< ${DATE_STRR//[-_]/ }
WEEK_AGO="${FCST_YY_R}-${FCST_MM_R}-${FCST_DD_R}_${FCST_HH_R}"

echo " Removing files from ${WEEK_AGO} (1 week ago): "

IFS=':' read -ra run_names <<<"$WRF_RUN_NAMES"

for run_name in "${run_names[@]}"; do 
  
  # wrfout files
  echo "${WRF_REALDIR}/${run_name}/wrfout_d01_${WEEK_AGO}_00_00_${WRF_FCST_DAYS}-day_fcst_rain"
  rm ${WRF_REALDIR}/${run_name}/wrfout_d01_${WEEK_AGO}_00_00_${WRF_FCST_DAYS}-day_fcst_rain 

  # ARWpost files
  echo "${WRF_POSTDIR}/${run_name}/wrffcst_d01_${WEEK_AGO} "
  rm ${WRF_POSTDIR}/${run_name}/wrffcst_d01_${WEEK_AGO}.*

  # Ensemble files
  echo "${WRF_ENS}/${run_name}/wrffcst_d01_${WEEK_AGO} "
  rm ${WRF_ENS}/${run_name}/wrffcst_d01_${WEEK_AGO}.*
  
done

# wrfout files
echo " wrf_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R} log files "
rm -f ${WRF_REALDIR}/wrf_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}_run*.log

echo " wrffcst_d01_${WEEK_AGO}_ens.nc "
echo " ens_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}.out "
# Ensemble files
rm -f ${WRF_ENS}/wrffcst_d01_${WEEK_AGO}_ens.nc
rm -f ${WRF_ENS}/ens_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}.out

echo " arw_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R} log files "
# ARWpost files
rm -f ${WRF_REALDIR}/arw_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}_run*.out

#cd ${WRF_REALDIR}
#conda activate toolbox
#ncks -O -v RAINC,RAINNC,Times,XLAT,XLONG wrfout_d01_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain wrfout_d01_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain
#ncks -O -v RAINC,RAINNC,Times,XLAT,XLONG wrfout_d02_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain wrfout_d02_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain
#conda deactivate toolbox


echo "------------------"
echo " Forecast finished! "
echo "------------------"
cd ${MAINDIR}
