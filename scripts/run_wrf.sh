#!/bin/bash

source $SCRIPT_DIR/set_env_wrf.run.sh

# -------------------------------------------- #
#     Link the ICBC in this model directory    #
# -------------------------------------------- #
cd ${WRF_REALDIR}
rm met_em.d0*
ln -s ${WRF_MAINDIR}/WPS/${NAMELIST_SUFF}/met_em.d0* .
for f in met_em.* ; do mv -v "$f" $(echo "$f" | tr ':' '_'); done

# -------------------------------------------- #
#             Edit namelist.input              #
# -------------------------------------------- #

rm -f namelist.input
sed -i "2s/.*/\ run_days                            = ${WRF_FCST_DAYS},/" namelist.input_${NAMELIST_SUFF}
sed -i "6s/.*/\ start_year                          = ${FCST_YY},${FCST_YY},/" namelist.input_${NAMELIST_SUFF}
sed -i "7s/.*/\ start_month                         = ${FCST_MM},${FCST_MM},/" namelist.input_${NAMELIST_SUFF}
sed -i "8s/.*/\ start_day                           = ${FCST_DD},${FCST_DD},/" namelist.input_${NAMELIST_SUFF}
sed -i "9s/.*/\ start_hour                          = ${FCST_ZZ},${FCST_ZZ},/" namelist.input_${NAMELIST_SUFF}
sed -i "12s/.*/\ end_year                            = ${FCST_YY2},${FCST_YY2},/" namelist.input_${NAMELIST_SUFF}
sed -i "13s/.*/\ end_month                           = ${FCST_MM2},${FCST_MM2},/" namelist.input_${NAMELIST_SUFF}
sed -i "14s/.*/\ end_day                             = ${FCST_DD2},${FCST_DD2},/" namelist.input_${NAMELIST_SUFF}
sed -i "15s/.*/\ end_hour                            = ${FCST_ZZ2},${FCST_ZZ2},/" namelist.input_${NAMELIST_SUFF}
ln -s namelist.input_${NAMELIST_SUFF} namelist.input

# -------------------------------------------- #
#                Run Real.exe                  #
# -------------------------------------------- #
echo "  ********************  "
echo " Running real "
echo "  ********************  "
rm -f wrfbdy* wrfinput* 
srun ./real.exe >& log.real & tail --pid=$! -f rsl.error.0000
echo "  ********************  "
echo " End of REAL "
echo "  ********************  "


# -------------------------------------------- #
#                Run WRF.exe                   #
# -------------------------------------------- #
echo "  ********************  "
echo " Running WRF "
echo "  ********************  "
srun ./wrf.exe >& log.wrf & tail --pid=$! -f rsl.error.0000
echo "  ********************  "
echo " End of WRF "
echo "  ********************  "


mv wrfout_d01_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}_00_00 wrfout_d01_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}_00_00_${WRF_FCST_DAYS}-day_fcst_rain
#mv wrfout_d02_${YY}-${mm}-${dd}_${FCST_ZZ}_00_00 wrfout_d02_${YY}-${mm}-${dd}_${FCST_ZZ}_00_00_${WRF_FCST_DAYS}-day_fcst_rain
