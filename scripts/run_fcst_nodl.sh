#!/bin/bash

echo "------------------"
echo " Starting WRF Forecast "
echo "------------------"

source $SCRIPT_DIR/set_date_vars.sh

mkdir -p $GFSDIR

# WPS
wps_slurm_opts="-A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES -J wps-$FCST_YYYYMMDD$FCST_ZZ -o $WRF_MAINDIR/WPS/wps_$FCST_YYYYMMDD$FCST_ZZ.out -n $SLURM_WPS_NTASKS"
wps_job_id=$(sbatch $wps_slurm_opts $SCRIPT_DIR/run_wps.sh)
wps_job_id=$(echo $wps_job_id | tr -dc '0-9')

# WRF
WRF_NTASKS=$SLURM_WRF_NTASKS
# H=$(date +%k)
# (( H < 9 || H > 15 )) && WRF_NTASKS=$SLURM_WRF_NTASKS2 || WRF_NTASKS=$SLURM_WRF_NTASKS
wrf_slurm_opts="-A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES -d afterok:$wps_job_id -J wrf-$FCST_YYYYMMDD$FCST_ZZ -o $WRF_MAINDIR/WRF/wrf_$FCST_YYYYMMDD$FCST_ZZ.out -n $WRF_NTASKS" # -B 2:24:1"
wrf_job_id=$(sbatch $wrf_slurm_opts $SCRIPT_DIR/run_wrf.sh)
wrf_job_id=$(echo $wrf_job_id | tr -dc '0-9')

# Post processing
arw_slurm_opts="-A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES -d afterok:$wrf_job_id -J arw-$FCST_YYYYMMDD$FCST_ZZ -o $WRF_MAINDIR/ARWpost/arw_$FCST_YYYYMMDD$FCST_ZZ.out -n 1"
arw_job_id=$(sbatch $arw_slurm_opts $SCRIPT_DIR/run_arwpost.sh)
arw_job_id=$(echo $arw_job_id | tr -dc '0-9')

# Upload
#  upload_slurm_opts="-A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES -d afterok:$arw_job_id -J upload-$FCST_YYYYMMDD$FCST_ZZ -o $MAINDIR/output/upload_$FCST_YYYYMMDD$FCST_ZZ.log -n 1"
#  upload_job_id=$(sbatch $upload_slurm_opts $SCRIPT_DIR/upload.sh)
#  upload_job_id=$(echo $upload_job_id | tr -dc '0-9')
