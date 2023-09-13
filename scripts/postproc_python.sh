#!/bin/bash

echo "---------------------------------"
echo " Starting python postprocessing! "
echo "---------------------------------"

# -------------------------------------------- #
#              Postprocessing                  #
# -------------------------------------------- #

export MPLBACKEND="agg"
export ESMFMKFILE="$CONDA_PREFIX/lib/esmf.mk"

cd "$SCRIPT_DIR/python" || exit
WRF_OUT_FILE="wrfout_d01_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}_00_00_5-day_fcst_rain"
${PYTHON} process_wrf.py -i "$WRF_OUT_FILE" -o "$OUTDIR"

echo "---------------------------------"
echo " Python postprocessing finished! "
echo "---------------------------------"
cd "$MAINDIR" || exit
