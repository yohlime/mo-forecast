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

sed -i "1s/.*/date='${DATE_STR1}PHT'/" wrf_rainfall_hourly.gs
sed -i "3s/.*/date2='${DATE_STR1} PHT'/" wrf_rainfall_hourly.gs
sed -i "1s/.*/date='${DATE_STR1}PHT'/" wrf_rainfall_hourly_metro_manila.gs
sed -i "3s/.*/date2='${DATE_STR1} PHT'/" wrf_rainfall_hourly_metro_manila.gs
sed -i "1s/.*/date='${DATE_STR1}PHT'/" clean_energy/clean_energy_comp.gs
sed -i "9s/.*/date2='${DATE_STR1} PHT'/" clean_energy/clean_energy_comp.gs
sed -i "1s/.*/date='${DATE_STR1}PHT'/" wrf_clim.gs
sed -i "9s/.*/date2='${DATE_STR1} PHT'/" wrf_clim.gs
DATE_STR2=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 32 hours" +'%Y-%m-%d_%H')
sed -i "2s/.*/d1title='${DATE_STR1} to ${DATE_STR2} PHT'/" clean_energy/clean_energy_comp.gs
sed -i "2s/.*/d1title='${DATE_STR1} to ${DATE_STR2} PHT'/" wrf_clim.gs
DATE_STR3=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 56 hours" +'%Y-%m-%d_%H')
sed -i "3s/.*/d2title='${DATE_STR2} to ${DATE_STR3} PHT'/" clean_energy/clean_energy_comp.gs
sed -i "3s/.*/d2title='${DATE_STR2} to ${DATE_STR3} PHT'/" wrf_clim.gs
DATE_STR4=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 80 hours" +'%Y-%m-%d_%H')
sed -i "4s/.*/d3title='${DATE_STR3} to ${DATE_STR4} PHT'/" clean_energy/clean_energy_comp.gs
sed -i "4s/.*/d3title='${DATE_STR3} to ${DATE_STR4} PHT'/" wrf_clim.gs
DATE_STR5=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 104 hours" +'%Y-%m-%d_%H')
sed -i "5s/.*/d4title='${DATE_STR4} to ${DATE_STR5} PHT'/" clean_energy/clean_energy_comp.gs
sed -i "5s/.*/d4title='${DATE_STR4} to ${DATE_STR5} PHT'/" wrf_clim.gs
DATE_STR6=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 128 hours" +'%Y-%m-%d_%H')
sed -i "6s/.*/d5title='${DATE_STR5} to ${DATE_STR6} PHT'/" clean_energy/clean_energy_comp.gs
sed -i "6s/.*/d5title='${DATE_STR5} to ${DATE_STR6} PHT'/" wrf_clim.gs


sed -i "7s~.*~outdir='${SCRIPT_DIR}/timeseries/csv'~" clean_energy/clean_energy_comp.gs
sed -i "7s~.*~outdir='${OUTDIR}/climatology/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}'~" wrf_clim.gs
sed -i "2s~.*~outdir='${OUTDIR}/hourly'~" wrf_rainfall_hourly.gs
sed -i "2s~.*~outdir='${OUTDIR}/hourly'~" wrf_rainfall_hourly_metro_manila.gs
sed -i "11s~.*~'sdfopen ${WRF_ENS}/${ARW_OUT_FILE}_ens.nc'~" clean_energy/clean_energy_comp.gs
sed -i "11s~.*~'sdfopen ${WRF_ENS}/${ARW_OUT_FILE}_ens.nc'~" wrf_clim.gs
sed -i "4s~.*~'sdfopen ${WRF_ENS}/${ARW_OUT_FILE}_ens.nc'~" wrf_rainfall_hourly.gs
sed -i "4s~.*~'sdfopen ${WRF_ENS}/${ARW_OUT_FILE}_ens.nc'~" wrf_rainfall_hourly_metro_manila.gs
sed -i "14s~.*~climdir='${MAINDIR}/climatology/frJulie/01_forForecasting'~" wrf_clim.gs
sed -i "15s~.*~month='${FCST_MM_PHT}'~" wrf_clim.gs
sed -i "16s~.*~monname='${FCST_MM_PHT2}'~" wrf_clim.gs

mkdir -p ${OUTDIR}/hourly/${FCST_YYYYMMDD}_${FCST_ZZ}
grads -pbc wrf_rainfall_hourly.gs

#create animation of hourly rainfall
convert -delay 20 -loop 0 ${OUTDIR}/hourly/first24/*.png ${OUTDIR}/hourly/first24/hourly_rainfall_${DATE_STR1}PHT.gif
mv ${OUTDIR}/hourly/first24/*.gif ${OUTDIR}/hourly/first24/*.png ${OUTDIR}/hourly/${FCST_YYYYMMDD}_${FCST_ZZ}/.
mv ${OUTDIR}/hourly/*.png ${OUTDIR}/hourly/${FCST_YYYYMMDD}_${FCST_ZZ}/.
mv ${OUTDIR}/hourly/${FCST_YYYYMMDD}_${FCST_ZZ}/*.gif ${OUTDIR}/hourly/.

#create hourly rain map over Metro Manila
grads -pbc wrf_rainfall_hourly_metro_manila.gs

#create animation of hourly rainfall over Metro Manila
convert -delay 20 -loop 0 ${OUTDIR}/hourly/first24/*.png ${OUTDIR}/hourly/first24/mnl_hourly_rainfall_${DATE_STR1}PHT.gif
mv ${OUTDIR}/hourly/first24/*.gif ${OUTDIR}/hourly/first24/*.png ${OUTDIR}/hourly/${FCST_YYYYMMDD}_${FCST_ZZ}/.
mv ${OUTDIR}/hourly/*.png ${OUTDIR}/hourly/${FCST_YYYYMMDD}_${FCST_ZZ}/.
mv ${OUTDIR}/hourly/${FCST_YYYYMMDD}_${FCST_ZZ}/*.gif ${OUTDIR}/hourly/.

# compare with climatology
mkdir -p ${OUTDIR}/climatology/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}
grads -pbc wrf_clim.gs

# ---------------------------------------------------------- #
#    Modify and run clean energy forecasting map scripts     #
# ---------------------------------------------------------- #

cd ${SCRIPT_DIR}/grads/clean_energy
grads -pbc clean_energy_comp.gs

# -------------------------------------------- #
#    Modify and run heat index map scripts     #
# -------------------------------------------- #

cd ${SCRIPT_DIR}/heat_index

sed -i "8s/.*/yyyymmdd = '${FCST_YY_PHT}-${FCST_MM_PHT}-${FCST_DD_PHT}'/" heat_index_netCDF.py
sed -i "9s/.*/init = '${FCST_HH_PHT}'/" heat_index_netCDF.py
sed -i "10s~.*~EXTRACT_DIR = '${SCRIPT_DIR}/grads/nc'~" heat_index_netCDF.py

# convert forecast rh and t2 to heat index, creating netCDF file
#PYTHONCONDA=/home/miniconda3/envs/toolbox/bin/python
$PYTHONCONDA heat_index_netCDF.py

# plot heat index via grads

cd ${SCRIPT_DIR}/grads
rm ${SCRIPT_DIR}/grads/nc/*.nc

# -------------------------------------------- #
#    Modify and run chance of rain scripts     #
# -------------------------------------------- #

cd ${SCRIPT_DIR}/rainchance

sed -i "1s/.*/date='${DATE_STR1}PHT'/" extract_rain.gs
sed -i "2s/.*/date2='${DATE_STR1} PHT'/" extract_rain.gs
sed -i "3s/.*/wrfrun='${ARW_OUT_FILE}'/" extract_rain.gs
sed -i "4s~.*~indir='${WRF_ENS}'~" extract_rain.gs
sed -i "5s~.*~outdir='${WRF_ENS}'~" extract_rain.gs

grads -pbc extract_rain.gs

sed -i "4s/.*/yyyymmdd = '${FCST_YY_PHT}-${FCST_MM_PHT}-${FCST_DD_PHT}'/" rainchance.py
sed -i "5s/.*/init = '${FCST_HH_PHT}'/" rainchance.py
sed -i "6s~.*~IN_DIR = '${WRF_ENS}'~" rainchance.py
sed -i "7s~.*~OUT_DIR = '${SCRIPT_DIR}/rainchance/nc'~" rainchance.py

$PYTHONCONDA rainchance.py

sed -i "1s/.*/date='${DATE_STR1}PHT'/" extract_chance.gs
sed -i "2s/.*/date2='${DATE_STR1} PHT'/" extract_chance.gs
sed -i "3s~.*~indir='${SCRIPT_DIR}/rainchance/nc'~" extract_chance.gs
sed -i "4s~.*~outdir='${SCRIPT_DIR}/rainchance/csv'~" extract_chance.gs

grads -pbc extract_chance.gs

sed -i "1s/.*/date='${DATE_STR1}PHT'/" extract_chance_cities.gs
sed -i "2s/.*/date2='${DATE_STR1} PHT'/" extract_chance_cities.gs
sed -i "3s~.*~indir='${SCRIPT_DIR}/rainchance/nc'~" extract_chance_cities.gs
sed -i "4s~.*~outdir='${SCRIPT_DIR}/rainchance/csv'~" extract_chance_cities.gs

grads -pbc extract_chance_cities.gs

# -------------------------------------------- #
#    Modify and run time series scripts        #
# -------------------------------------------- #
cd ${SCRIPT_DIR}/grads/extract

sed -i "1s/.*/date='${DATE_STR1}PHT'/" extract_data.gs
sed -i "2s~.*~'sdfopen ${WRF_ENS}/${ARW_OUT_FILE}_ens.nc'~" extract_data.gs
sed -i "3s~.*~outdir='${SCRIPT_DIR}/timeseries/csv'~" extract_data.gs
sed -i "53s~.*~'sdfopen ${WRF_ENS}/${ARW_OUT_FILE}_ens.nc'~" extract_data.gs

grads -pbc extract_data.gs

sed -i "1s/.*/date='${DATE_STR1}PHT'/" extract_cities.gs
sed -i "2s~.*~'sdfopen ${WRF_ENS}/${ARW_OUT_FILE}_ens.nc'~" extract_cities.gs
sed -i "3s~.*~outdir='${SCRIPT_DIR}/timeseries/csv'~" extract_cities.gs
sed -i "53s~.*~'sdfopen ${WRF_ENS}/${ARW_OUT_FILE}_ens.nc'~" extract_cities.gs

grads -pbc extract_cities.gs

cd ${SCRIPT_DIR}/timeseries
sed -i "4s/.*/yyyymmdd = '${FCST_YY_PHT}-${FCST_MM_PHT}-${FCST_DD_PHT}'/" concat_csv_fcst.py
sed -i "5s/.*/init = '${FCST_HH_PHT}'/" concat_csv_fcst.py
sed -i "6s~.*~OUT_DIR = '${OUTDIR}/timeseries/csv/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}'~" concat_csv_fcst.py
sed -i "7s~.*~IN_DIR = '${SCRIPT_DIR}/timeseries'~" concat_csv_fcst.py

sed -i "4s/.*/yyyymmdd = '${FCST_YY_PHT}-${FCST_MM_PHT}-${FCST_DD_PHT}'/" concat_csv_ce.py
sed -i "5s/.*/init = '${FCST_HH_PHT}'/" concat_csv_ce.py
sed -i "6s~.*~OUT_DIR = '${OUTDIR}/summary/clean_energy/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}'~" concat_csv_ce.py
sed -i "7s~.*~IN_DIR = '${SCRIPT_DIR}/timeseries'~" concat_csv_ce.py

sed -i "4s/.*/yyyymmdd = '${FCST_YY_PHT}-${FCST_MM_PHT}-${FCST_DD_PHT}'/" summary.py
sed -i "5s/.*/init = '${FCST_HH_PHT}'/" summary.py
sed -i "6s~.*~OUT_DIR = '${OUTDIR}/summary/csv/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}'~" summary.py
sed -i "7s~.*~IN_DIR = '${OUTDIR}/timeseries/csv/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}'~" summary.py
sed -i "8s~.*~ST_DIR = '${SCRIPT_DIR}/timeseries/csv'~" summary.py
sed -i "9s~.*~CH_DIR = '${SCRIPT_DIR}/rainchance/csv'~" summary.py

sed -i "4s/.*/yyyymmdd = '${FCST_YY_PHT}-${FCST_MM_PHT}-${FCST_DD_PHT}'/" concat_csv_cities.py
sed -i "5s/.*/init = '${FCST_HH_PHT}'/" concat_csv_cities.py
sed -i "6s~.*~OUT_DIR = '${OUTDIR}/timeseries/csv_cities/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}'~" concat_csv_cities.py
sed -i "7s~.*~IN_DIR = '${SCRIPT_DIR}/timeseries'~" concat_csv_cities.py

sed -i "4s/.*/yyyymmdd = '${FCST_YY_PHT}-${FCST_MM_PHT}-${FCST_DD_PHT}'/" summary_cities.py
sed -i "5s/.*/init = '${FCST_HH_PHT}'/" summary_cities.py
sed -i "6s~.*~OUT_DIR = '${OUTDIR}/summary/json/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}'~" summary_cities.py
sed -i "7s~.*~IN_DIR = '${OUTDIR}/timeseries/csv_cities/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}'~" summary_cities.py
sed -i "8s~.*~ST_DIR = '${SCRIPT_DIR}/timeseries/csv'~" summary_cities.py
sed -i "9s~.*~CH_DIR = '${SCRIPT_DIR}/rainchance/csv'~" summary_cities.py

#organize forecast csv input and plot time series

#conda activate toolbox

#PYTHONCONDA=/home/miniconda3/envs/toolbox/bin/python
$PYTHONCONDA concat_csv_fcst.py
$PYTHONCONDA concat_csv_ce.py
$PYTHONCONDA summary.py

$PYTHONCONDA concat_csv_cities.py
$PYTHONCONDA summary_cities.py

rm ${SCRIPT_DIR}/timeseries/csv/${DATE_STR1}PHT*.csv

#conda deactivate

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

# Delete rain chance files
rm -f ${SCRIPT_DIR}/rainchance/csv/${DATE_STR1}PHT*chance.csv
rm -f ${SCRIPT_DIR}/rainchance/nc/rainchance_day*${DATE_STR1}PHT.nc

# ------------------------------- #
#        Delete past files        #
# ------------------------------- #

# Remove files from 1 month ago
DATE_STRR=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 1 month ago" +'%Y-%m-%d_%H')
read FCST_YY_R FCST_MM_R FCST_DD_R FCST_HH_R <<< ${DATE_STRR//[-_]/ }
MONTH_AGO="${FCST_YY_R}-${FCST_MM_R}-${FCST_DD_R}_${FCST_HH_R}"

# GFS log file
rm -f $MAINDIR/input/gfs_files/gfs_dload_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}.log

# WPS log file
rm -f ${WRF_MAINDIR}/WPS/wps_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}.out

# ARWpost files
rm -f ${WRF_POSTDIR}/${WRF_NAMELIST_SUFF1}/wrffcst_d01_${MONTH_AGO}.*
rm -f ${WRF_POSTDIR}/${WRF_NAMELIST_SUFF2}/wrffcst_d01_${MONTH_AGO}.*
rm -f ${WRF_POSTDIR}/${WRF_NAMELIST_SUFF3}/wrffcst_d01_${MONTH_AGO}.*
rm -f ${WRF_REALDIR}/arw_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}_run*.out

# Remove files from 1 week ago
DATE_STRR=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 1 week ago" +'%Y-%m-%d_%H')
read FCST_YY_R FCST_MM_R FCST_DD_R FCST_HH_R <<< ${DATE_STRR//[-_]/ }
WEEK_AGO="${FCST_YY_R}-${FCST_MM_R}-${FCST_DD_R}_${FCST_HH_R}"

# wrfout files
rm -f ${WRF_REALDIR}/${WRF_NAMELIST_SUFF1}/wrfout_d01_${WEEK_AGO}_00_00_${WRF_FCST_DAYS}-day_fcst_rain
rm -f ${WRF_REALDIR}/${WRF_NAMELIST_SUFF2}/wrfout_d01_${WEEK_AGO}_00_00_${WRF_FCST_DAYS}-day_fcst_rain
rm -f ${WRF_REALDIR}/${WRF_NAMELIST_SUFF3}/wrfout_d01_${WEEK_AGO}_00_00_${WRF_FCST_DAYS}-day_fcst_rain
rm -f ${WRF_REALDIR}/wrf_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}_run*.log

# Ensemble files
rm -f ${WRF_ENS}/wrffcst_d01_${WEEK_AGO}_ens.nc
rm -f ${WRF_ENS}/ens_${FCST_YY_R}${FCST_MM_R}${FCST_DD_R}${FCST_HH_R}.out

#cd ${WRF_REALDIR}
#conda activate toolbox
#ncks -O -v RAINC,RAINNC,Times,XLAT,XLONG wrfout_d01_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain wrfout_d01_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain
#ncks -O -v RAINC,RAINNC,Times,XLAT,XLONG wrfout_d02_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain wrfout_d02_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain
#conda deactivate toolbox


echo "------------------"
echo " Forecast finished! "
echo "------------------"
cd ${MAINDIR}
