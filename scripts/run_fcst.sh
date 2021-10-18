#!/bin/bash

DOWNLOAD_INPUT=true
UPLOAD_OUTPUT=true
POST_PROCESS=true

while [ True ]; do
if [ "$1" = "--no-download"]; then
    DOWNLOAD_INPUT=false
    shift 1
elif [ "$1" = "--no-upload"]; then
    UPLOAD_OUTPUT=false
    shift 1
elif [ "$1" = "--no-post-proc"]; then
    POST_PROCESS=false
    shift 1
else
    break
fi
done

echo "------------------"
echo " Starting WRF Forecast "
echo "------------------"

source $SCRIPT_DIR/set_date_vars.sh

mkdir -p $GFSDIR

if [ "$DOWNLOAD_INPUT" = true ]; then
  # download GFS
  source $SCRIPT_DIR/download_gfs.aria2.sh
fi

NDL_FILES=$(ls $GFSDIR/*.grb | wc -l)

if [ $NDL_FILES -eq $NUM_FILES ]; then

  # WPS
  slurm_opts="-A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES -J wps-$FCST_YYYYMMDD$FCST_ZZ -o $WRF_MAINDIR/WPS/wps_$FCST_YYYYMMDD$FCST_ZZ.out -n $SLURM_WPS_NTASKS"
  prev_jid=$(sbatch $slurm_opts $SCRIPT_DIR/run_wps.sh)
  prev_jid=$(echo $prev_jid | tr -dc '0-9')

  # WRF
  # schedule multiple slurm WRF jobs based on WRF_RUN_NAMES
  run_idx=1
  while IFS=':' read -ra RUN_NAMES; do
    for run_name in "${RUN_NAMES[@]}"; do
      export NAMELIST_RUN=$run_name

      WRF_NTASKS=$SLURM_WRF_NTASKS
      slurm_opts="-A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES -d afterok:$prev_jid -J wrf-$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx} -o $WRF_MAINDIR/WRF/wrf_$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx}.out -n $WRF_NTASKS -c $SLURM_WRF_CPUS_PER_TASK"
      prev_jid=$(sbatch $slurm_opts $SCRIPT_DIR/run_wrf.sh)
      prev_jid=$(echo $prev_jid | tr -dc '0-9')

      run_idx=$((run_idx+1))
    done
  done <<< "$WRF_RUN_NAMES"

  if [ "$POST_PROCESS" = true ]; then
    # Post processing

    ### Python Post processing
    slurm_opts="-A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES -d afterok:$prev_jid -J python-$FCST_YYYYMMDD$FCST_ZZ -o ${OUTDIR}/logs/python/python_$FCST_YYYYMMDD$FCST_ZZ.out -n 12"
    prev_jid=$(sbatch $slurm_opts $SCRIPT_DIR/postproc_python.sh)
    prev_jid=$(echo $prev_jid | tr -dc '0-9')

    if [ "$UPLOAD_OUTPUT" = true ]; then
      ### Web Upload
      slurm_opts="-A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES -d afterok:$prev_jid -J web-upload-$FCST_YYYYMMDD$FCST_ZZ -o $MAINDIR/output/web-upload_$FCST_YYYYMMDD$FCST_ZZ.log -n 1"
      sbatch $slurm_opts $SCRIPT_DIR/web_upload.sh
    fi

    ### ARWpost
    ### schedule multiple slurm ARWpost jobs based on WRF_RUN_NAMES
    run_idx=1
    while IFS=':' read -ra RUN_NAMES; do
      for run_name in "${RUN_NAMES[@]}"; do
        export NAMELIST_RUN=$run_name

        slurm_opts="-A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES -d afterok:$prev_jid -J arw-$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx} -o $WRF_MAINDIR/ARWpost/arw_$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx}.out -n 1"
        prev_jid=$(sbatch $slurm_opts $SCRIPT_DIR/run_arwpost.sh)
        prev_jid=$(echo $prev_jid | tr -dc '0-9')

        run_idx=$((run_idx+1))
      done
    done <<< "$WRF_RUN_NAMES"

    ### ENSEMBLE Post processing
    ens_slurm_opts="-A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES -d afterok:$prev_jid -J ens-$FCST_YYYYMMDD$FCST_ZZ -o $WRF_MAINDIR/ENSEMBLE/ens_$FCST_YYYYMMDD$FCST_ZZ.out -n 1"
    sbatch $ens_slurm_opts $SCRIPT_DIR/run_post_ens.sh
  fi

fi
