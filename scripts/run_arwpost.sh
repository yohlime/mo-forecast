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
ln -sf ${WRF_REALDIR}/${NAMELIST_RUN}/${WRF_OUT_FILE} ${WRF_POSTDIR}/.


# -------------------------------------------- #
#          Modify namelist.ARWpost_fcst        #
# -------------------------------------------- #
rm -f namelist.ARWpost
sed -i "2s/.*/\ start_date = '${ARW_START_DATE}',/" namelist.ARWpost_${NAMELIST_RUN}
sed -i "3s/.*/\ end_date   = '${ARW_END_DATE}',/" namelist.ARWpost_${NAMELIST_RUN}
sed -i "10s/.*/\ input_root_name    = '\.\/${WRF_OUT_FILE}',/" namelist.ARWpost_${NAMELIST_RUN}
sed -i "11s/.*/\ output_root_name   = '\.\/${ARW_OUT_FILE}',/" namelist.ARWpost_${NAMELIST_RUN}
ln -s namelist.ARWpost_${NAMELIST_RUN} namelist.ARWpost

echo "------------------"
echo " Postprocessing... "
echo "------------------"
rm -f *.ctl
rm -f *.dat
srun ./ARWpost.exe >& log.ARWpost & tail --pid=$! -f log.ARWpost
mkdir -p ${NAMELIST_RUN}
mv wrffcst* ${NAMELIST_RUN}/


echo "-----------------------------------------"
echo " ARWpost for ${NAMELIST_RUN} finished!   "
echo "-----------------------------------------"
#cd ${MAINDIR}
