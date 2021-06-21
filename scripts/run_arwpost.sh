#!/bin/bash

source $SCRIPT_DIR/set_env_wrf.run.sh

# -------------------------------------------- #
#              Postprocessing                  #
# -------------------------------------------- #
cd ${WRF_POSTDIR}

WRF_OUT_FILE="wrfout_d01_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}_00_00_${WRF_FCST_DAYS}-day_fcst_rain"
ARW_OUT_FILE="wrffcst_d01_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}"
ARW_START_DATE="${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}:00:00"
ARW_END_DATE="${FCST_YY2}-${FCST_MM2}-${FCST_DD2}_${FCST_ZZ2}:00:00"


# -------------------------------------------- #
#           Link output file here              #
# -------------------------------------------- #
rm -f ${WRF_POSTDIR}/wrfout_*fcst_rain
ln -sf ${WRF_REALDIR}/${WRF_OUT_FILE} ${WRF_POSTDIR}/.


# -------------------------------------------- #
#          Modify namelist.ARWpost_fcst        #
# -------------------------------------------- #
rm -f namelist.ARWpost
sed -i "2s/.*/\ start_date = '${ARW_START_DATE}',/" namelist.ARWpost_${NAMELIST_SUFF}
sed -i "3s/.*/\ end_date   = '${ARW_END_DATE}',/" namelist.ARWpost_${NAMELIST_SUFF}
sed -i "10s/.*/\ input_root_name    = '\.\/${WRF_OUT_FILE}',/" namelist.ARWpost_${NAMELIST_SUFF}
sed -i "11s/.*/\ output_root_name   = '\.\/${ARW_OUT_FILE}',/" namelist.ARWpost_${NAMELIST_SUFF}
ln -s namelist.ARWpost_${NAMELIST_SUFF} namelist.ARWpost

echo "------------------"
echo " Postprocessing... "
echo "------------------"
rm -f *.ctl
rm -f *.dat
srun ./ARWpost.exe >& log.ARWpost & tail --pid=$! -f log.ARWpost
mkdir -p ${NAMELIST_SUFF}
mv wrffcst* ${NAMELIST_SUFF}/
cd ${MAINDIR}/scripts/grads

DATE_STR1=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 8 hours" +'%Y-%m-%d_%H')
read FCST_YY_PHT FCST_MM_PHT FCST_DD_PHT FCST_HH_PHT <<< ${DATE_STR1//[-_]/ }

sed -i "1s/.*/date='${DATE_STR1}PHT'/" wrf_var.gs
sed -i "9s/.*/date2='${DATE_STR1} PHT'/" wrf_var.gs
sed -i "1s/.*/date='${DATE_STR1}PHT'/" wrf_rainfall_hourly.gs
sed -i "9s/.*/date2='${DATE_STR1} PHT'/" wrf_rainfall_hourly.gs
sed -i "1s/.*/date='${DATE_STR1}PHT'/" wrf_rainfall_hourly_metro_manila.gs
sed -i "9s/.*/date2='${DATE_STR1} PHT'/" wrf_rainfall_hourly_metro_manila.gs
sed -i "1s/.*/date='${DATE_STR1}PHT'/" wrf_HI.gs
sed -i "9s/.*/date2='${DATE_STR1} PHT'/" wrf_HI.gs
sed -i "1s/.*/date='${DATE_STR1}PHT'/" clean_energy/ghi.gs
sed -i "9s/.*/date2='${DATE_STR1} PHT'/" clean_energy/ghi.gs
sed -i "1s/.*/date='${DATE_STR1}PHT'/" clean_energy/solar_power.gs
sed -i "9s/.*/date2='${DATE_STR1} PHT'/" clean_energy/solar_power.gs
sed -i "1s/.*/date='${DATE_STR1}PHT'/" clean_energy/wind_power.gs
sed -i "9s/.*/date2='${DATE_STR1} PHT'/" clean_energy/wind_power.gs
DATE_STR2=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 32 hours" +'%Y-%m-%d_%H')
sed -i "2s/.*/d1title='${DATE_STR1} to ${DATE_STR2} PHT'/" wrf_var.gs
sed -i "2s/.*/d1title='${DATE_STR1} to ${DATE_STR2} PHT'/" wrf_HI.gs
sed -i "2s/.*/d1title='${DATE_STR1} to ${DATE_STR2} PHT'/" clean_energy/ghi.gs
sed -i "2s/.*/d1title='${DATE_STR1} to ${DATE_STR2} PHT'/" clean_energy/solar_power.gs
sed -i "2s/.*/d1title='${DATE_STR1} to ${DATE_STR2} PHT'/" clean_energy/wind_power.gs
DATE_STR3=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 56 hours" +'%Y-%m-%d_%H')
sed -i "3s/.*/d2title='${DATE_STR2} to ${DATE_STR3} PHT'/" wrf_var.gs
sed -i "3s/.*/d2title='${DATE_STR2} to ${DATE_STR3} PHT'/" wrf_HI.gs
sed -i "3s/.*/d2title='${DATE_STR2} to ${DATE_STR3} PHT'/" clean_energy/ghi.gs
sed -i "3s/.*/d2title='${DATE_STR2} to ${DATE_STR3} PHT'/" clean_energy/solar_power.gs
sed -i "3s/.*/d2title='${DATE_STR2} to ${DATE_STR3} PHT'/" clean_energy/wind_power.gs
DATE_STR4=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 80 hours" +'%Y-%m-%d_%H')
sed -i "4s/.*/d3title='${DATE_STR3} to ${DATE_STR4} PHT'/" wrf_var.gs
sed -i "4s/.*/d3title='${DATE_STR3} to ${DATE_STR4} PHT'/" wrf_HI.gs
sed -i "4s/.*/d3title='${DATE_STR3} to ${DATE_STR4} PHT'/" clean_energy/ghi.gs
sed -i "4s/.*/d3title='${DATE_STR3} to ${DATE_STR4} PHT'/" clean_energy/solar_power.gs
sed -i "4s/.*/d3title='${DATE_STR3} to ${DATE_STR4} PHT'/" clean_energy/wind_power.gs
DATE_STR5=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 104 hours" +'%Y-%m-%d_%H')
sed -i "5s/.*/d4title='${DATE_STR4} to ${DATE_STR5} PHT'/" wrf_var.gs
sed -i "5s/.*/d4title='${DATE_STR4} to ${DATE_STR5} PHT'/" wrf_HI.gs
sed -i "5s/.*/d4title='${DATE_STR4} to ${DATE_STR5} PHT'/" clean_energy/ghi.gs
sed -i "5s/.*/d4title='${DATE_STR4} to ${DATE_STR5} PHT'/" clean_energy/solar_power.gs
sed -i "5s/.*/d4title='${DATE_STR4} to ${DATE_STR5} PHT'/" clean_energy/wind_power.gs
DATE_STR6=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00 128 hours" +'%Y-%m-%d_%H')
sed -i "6s/.*/d5title='${DATE_STR5} to ${DATE_STR6} PHT'/" wrf_var.gs
sed -i "6s/.*/d5title='${DATE_STR5} to ${DATE_STR6} PHT'/" wrf_HI.gs
sed -i "6s/.*/d5title='${DATE_STR5} to ${DATE_STR6} PHT'/" clean_energy/ghi.gs
sed -i "6s/.*/d5title='${DATE_STR5} to ${DATE_STR6} PHT'/" clean_energy/solar_power.gs
sed -i "6s/.*/d5title='${DATE_STR5} to ${DATE_STR6} PHT'/" clean_energy/wind_power.gs

sed -i "7s~.*~outdir='${OUTDIR}/maps'~" wrf_var.gs
sed -i "7s~.*~outdir='${OUTDIR}/maps'~" wrf_HI.gs
sed -i "7s~.*~outdir='${OUTDIR}/maps'~" clean_energy/ghi.gs
sed -i "7s~.*~outdir='${OUTDIR}/maps'~" clean_energy/solar_power.gs
sed -i "7s~.*~outdir='${OUTDIR}/maps'~" clean_energy/wind_power.gs
sed -i "2s~.*~outdir='${OUTDIR}/hourly'~" wrf_rainfall_hourly.gs
sed -i "2s~.*~outdir='${OUTDIR}/hourly'~" wrf_rainfall_hourly_metro_manila.gs
sed -i "11s~.*~'open ${WRF_POSTDIR}/${NAMELIST_SUFF}/${ARW_OUT_FILE}.ctl'~" wrf_var.gs
sed -i "11s~.*~'open ${WRF_POSTDIR}/${NAMELIST_SUFF}/${ARW_OUT_FILE}.ctl'~" clean_energy/ghi.gs
sed -i "11s~.*~'open ${WRF_POSTDIR}/${NAMELIST_SUFF}/${ARW_OUT_FILE}.ctl'~" clean_energy/solar_power.gs
sed -i "11s~.*~'open ${WRF_POSTDIR}/${NAMELIST_SUFF}/${ARW_OUT_FILE}.ctl'~" clean_energy/wind_power.gs
sed -i "4s~.*~'open ${WRF_POSTDIR}/${NAMELIST_SUFF}/${ARW_OUT_FILE}.ctl'~" wrf_rainfall_hourly.gs
sed -i "4s~.*~'open ${WRF_POSTDIR}/${NAMELIST_SUFF}/${ARW_OUT_FILE}.ctl'~" wrf_rainfall_hourly_metro_manila.gs
sed -i "11s~.*~'sdfopen ${SCRIPT_DIR}/grads/nc/wrf-HI_${DATE_STR1}PHT.nc'~" wrf_HI.gs

grads -pbc wrf_var.gs
#mv *.tif ${OUTDIR}/tif

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

# ---------------------------------------------------------- #
#    Modify and run clean energy forecasting map scripts     #
# ---------------------------------------------------------- #

cd ${SCRIPT_DIR}/grads/clean_energy
grads -pbc ghi.gs
grads -pbc solar_power.gs
grads -pbc wind_power.gs

# -------------------------------------------- #
#    Modify and run heat index map scripts     #
# -------------------------------------------- #

cd ${SCRIPT_DIR}/heat_index

sed -i "8s/.*/yyyymmdd = '${FCST_YY_PHT}-${FCST_MM_PHT}-${FCST_DD_PHT}'/" heat_index_netCDF.py
sed -i "9s/.*/init = '${FCST_HH_PHT}'/" heat_index_netCDF.py
sed -i "10s~.*~EXTRACT_DIR = '${SCRIPT_DIR}/grads/nc'~" heat_index_netCDF.py

# convert forecast rh and t2 to heat index, creating netCDF file
PYTHONCONDA=/home/miniconda3/envs/toolbox/bin/python
$PYTHONCONDA heat_index_netCDF.py

# plot heat index via grads

cd ${SCRIPT_DIR}/grads
grads -pbc wrf_HI.gs
rm ${SCRIPT_DIR}/grads/nc/*.nc

# -------------------------------------------- #
#    Modify and run time series scripts        #
# -------------------------------------------- #
cd ${SCRIPT_DIR}/grads/extract

sed -i "1s/.*/date='${DATE_STR1}PHT'/" extract_data.gs
sed -i "2s~.*~'open ${WRF_POSTDIR}/${NAMELIST_SUFF}/${ARW_OUT_FILE}.ctl'~" extract_data.gs
sed -i "3s~.*~outdir='${SCRIPT_DIR}/timeseries/csv'~" extract_data.gs
sed -i "53s~.*~'open ${WRF_POSTDIR}/${NAMELIST_SUFF}/${ARW_OUT_FILE}.ctl'~" extract_data.gs

grads -pbc extract_data.gs

cd ${SCRIPT_DIR}/timeseries
sed -i "4s/.*/yyyymmdd = '${FCST_YY_PHT}-${FCST_MM_PHT}-${FCST_DD_PHT}'/" concat_csv_fcst.py
sed -i "5s/.*/init = '${FCST_HH_PHT}'/" concat_csv_fcst.py
sed -i "6s~.*~OUT_DIR = '${OUTDIR}/timeseries/csv/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}'~" concat_csv_fcst.py
sed -i "7s~.*~IN_DIR = '${SCRIPT_DIR}/timeseries'~" concat_csv_fcst.py

sed -i "8s/.*/yyyymmdd = '${FCST_YY_PHT}-${FCST_MM_PHT}-${FCST_DD_PHT}'/" timeseries_plots.py
sed -i "9s/.*/init = '${FCST_HH_PHT}'/" timeseries_plots.py
sed -i "10s/.*/mm = ${FCST_MM_PHT#0}/" timeseries_plots.py
sed -i "11s~.*~OUT_DIR = '${OUTDIR}/timeseries'~" timeseries_plots.py
sed -i "12s~.*~IN_DIR = '${OUTDIR}/timeseries/csv/${FCST_YY}${FCST_MM}${FCST_DD}/${FCST_ZZ}'~" timeseries_plots.py
sed -i "13s/.*/stn_id = 'MOIP'/" timeseries_plots.py
sed -i "14s/.*/station_name = 'Manila Observatory'/" timeseries_plots.py

#organize forecast csv input and plot time series

#conda activate toolbox

PYTHONCONDA=/home/miniconda3/envs/toolbox/bin/python
$PYTHONCONDA concat_csv_fcst.py
export MPLBACKEND="agg"; $PYTHONCONDA timeseries_plots.py

rm ${SCRIPT_DIR}/timeseries/csv/${DATE_STR1}PHT*.csv

#conda deactivate

echo "------------------"
echo " Finished postprocessing! "
echo "------------------"

cd ${WRF_REALDIR}
#conda activate toolbox
#ncks -O -v RAINC,RAINNC,Times,XLAT,XLONG wrfout_d01_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain wrfout_d01_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain
#ncks -O -v RAINC,RAINNC,Times,XLAT,XLONG wrfout_d02_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain wrfout_d02_${YY}-${mm}-${dd}_${HH}_00_00_${fcst_days}-day_fcst_rain
#conda deactivate toolbox

# Remove file from 3 months ago to ensure no pile up
#DATE3=$(date -d "$YY-$mm-${dd} $FCST_ZZ:00:00 3 months ago" +'%Y-%m-%d %H:%M:%S')
#read YY3 mm3 dd3 HH3 MM3 SS3 <<< ${DATE3//[-: ]/ }
#rm -f wrfout_d01_${YY3}-${mm3}-${dd3}_${HH3}_00_00_${fcst_days}-day_fcst_rain wrfout_d02_${YY3}-${mm3}-${dd3}_${HH3}_00_00_${fcst_days}-day_fcst_rain

echo "------------------"
echo " Forecast finished! "
echo "------------------"
cd ${MAINDIR}
