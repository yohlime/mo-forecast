#!/bin/bash

#################### CONSTANTS ####################
DOWNLOAD_INPUT=1
DOWNLOAD_MADIS=1
UPLOAD_OUTPUT=1
POST_PROCESS=1
SLURM_OPTS0="-A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES"
###################################################

#################### FUNCTIONS ####################
function show_usage() {
  printf "Usage: $0 [options [parameters]]\n"
  printf "\n"
  printf "Options:\n"
  printf " --no-download, Do not download WRF inputs (GFS, etc...)\n"
  printf " --no-download-madis, Do not download 3DVAR inputs (MADIS, etc...)\n"
  printf " --no-upload, Do not upload outputs\n"
  printf " --no-post-proc, No post processing\n"
  printf " -h|--help, Print help\n"

  return 0
}

function submit_job() {
  jid=$(sbatch $1)
  echo $jid | tr -dc '0-9'
  return 0
}
###################################################

################### PROCESS ARGS ###################
while [ ! -z "$1" ]; do
  case "$1" in
    --no-download)
      DOWNLOAD_INPUT=0
      ;;
    --no-download-madis)
      DOWNLOAD_MADIS=0
      ;;
    --no-upload)
      UPLOAD_OUTPUT=0
      ;;
    --no-post-proc)
      POST_PROCESS=0
      ;;
    *)
      show_usage
      ;;
  esac
  shift
done
###################################################

echo "------------------"
echo " Starting WRF Forecast "
echo "------------------"

source $SCRIPT_DIR/set_date_vars.sh

mkdir -p $GFSDIR

if [ $DOWNLOAD_INPUT -eq 1 ]; then
  # download GFS
  source $SCRIPT_DIR/download_gfs.aria2.sh
fi

if [ $DOWNLOAD_MADIS -eq 1 ]; then
  # download MADIS 
  source $SCRIPT_DIR/download_madis.aria2.sh
fi

NDL_FILES=$(ls $GFSDIR/*.grb | wc -l)

if [ $NDL_FILES -eq $NUM_FILES ]; then

  # WPS
  slurm_opts="$SLURM_OPTS0"
  slurm_opts="$slurm_opts -J wps-$FCST_YYYYMMDD$FCST_ZZ"
  slurm_opts="$slurm_opts -o $WRF_MAINDIR/WPS/wps_$FCST_YYYYMMDD$FCST_ZZ.out"
  slurm_opts="$slurm_opts -n $SLURM_WPS_NTASKS"
  prev_jid=$(submit_job "$slurm_opts $SCRIPT_DIR/run_wps.sh")

  # WRF
  # schedule multiple slurm WRF jobs based on WRF_RUN_NAMES
  run_idx=1
  while IFS=':' read -ra RUN_NAMES; do
    IFS=':' read -ra run3dvar <<< "$WRFDA_RUN_NAMES"

    for run_name in "${RUN_NAMES[@]}"; do
      export NAMELIST_3DVar=${run3dvar[$run_idx -1]}
      export NAMELIST_RUN=$run_name

      WRF_NTASKS=$SLURM_WRF_NTASKS
      slurm_opts="$SLURM_OPTS0"
      slurm_opts="$slurm_opts -d afterok:$prev_jid"
      slurm_opts="$slurm_opts -J wrf-$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx}"
      slurm_opts="$slurm_opts -o $WRF_MAINDIR/WRF/wrf_$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx}.out"
      slurm_opts="$slurm_opts -n $WRF_NTASKS"
      slurm_opts="$slurm_opts -c $SLURM_WRF_CPUS_PER_TASK"
      prev_jid=$(submit_job "$slurm_opts $SCRIPT_DIR/run_wrf3dvar.sh")

      run_idx=$((run_idx+1))
    done
  done <<< "$WRF_RUN_NAMES"

  if [ $POST_PROCESS -eq 1 ]; then
    # Post processing

    ### Python Post processing
    slurm_opts="$SLURM_OPTS0"
    slurm_opts="$slurm_opts -d afterok:$prev_jid"
    slurm_opts="$slurm_opts -J python-$FCST_YYYYMMDD$FCST_ZZ"
    slurm_opts="$slurm_opts -o ${OUTDIR}/logs/python/python_$FCST_YYYYMMDD$FCST_ZZ.out"
    slurm_opts="$slurm_opts -n 12"
    prev_jid=$(submit_job "$slurm_opts $SCRIPT_DIR/postproc_python.sh")

    if [ $UPLOAD_OUTPUT -eq 1 ]; then
      ### Web Upload
      slurm_opts=$SLURM_OPTS0
      slurm_opts="$slurm_opts -d afterok:$prev_jid"
      slurm_opts="$slurm_opts -J web-upload-$FCST_YYYYMMDD$FCST_ZZ"
      slurm_opts="$slurm_opts -o $MAINDIR/output/web-upload_$FCST_YYYYMMDD$FCST_ZZ.log"
      slurm_opts="$slurm_opts -n 1"
      prev_jid=$(submit_job "$slurm_opts $SCRIPT_DIR/web_upload.sh")
    fi

    ### ARWpost
    ### schedule multiple slurm ARWpost jobs based on WRF_RUN_NAMES
    run_idx=1
    while IFS=':' read -ra RUN_NAMES; do
      for run_name in "${RUN_NAMES[@]}"; do
        export NAMELIST_RUN=$run_name

        slurm_opts=$SLURM_OPTS0
        slurm_opts="$slurm_opts -d afterok:$prev_jid"
        slurm_opts="$slurm_opts -J arw-$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx}"
        slurm_opts="$slurm_opts -o $WRF_MAINDIR/ARWpost/arw_$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx}.out"
        slurm_opts="$slurm_opts -n 1"
        prev_jid=$(submit_job "$slurm_opts $SCRIPT_DIR/run_arwpost.sh")

        run_idx=$((run_idx+1))
      done
    done <<< "$WRF_RUN_NAMES"

    ### ENSEMBLE Post processing
    slurm_opts=$SLURM_OPTS0
    slurm_opts="$slurm_opts -d afterok:$prev_jid"
    slurm_opts="$slurm_opts -J ens-$FCST_YYYYMMDD$FCST_ZZ"
    slurm_opts="$slurm_opts -o $WRF_MAINDIR/ENSEMBLE/ens_$FCST_YYYYMMDD$FCST_ZZ.out"
    slurm_opts="$slurm_opts -n 1"
    prev_jid=$(submit_job "$slurm_opts $SCRIPT_DIR/run_post_ens.sh")
  fi

fi