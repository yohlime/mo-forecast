#!/bin/bash

source $SCRIPT_DIR/set_env_wrf.run.sh
PYTHONCONDA=/home/miniconda3/envs/toolbox/bin/python
PYTHONPATH=$SCRIPT_DIR/python:${PYTHONPATH}
MPLBACKEND="agg"

WRF_OUT_FILE="wrfout_d01_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}_00_00_5-day_fcst_rain"


echo "---------------------------------"
echo " Starting python postprocessing! "
echo "---------------------------------"


# -------------------------------------------- #
#              Postprocessing                  #
# -------------------------------------------- #

cd $SCRIPT_DIR/python
$PYTHONCONDA process_wrf.py -i ${WRF_OUT_FILE} -o ${OUTDIR}/.test

echo "---------------------------------"
echo " Python postprocessing finished! "
echo "---------------------------------"
cd ${MAINDIR}
