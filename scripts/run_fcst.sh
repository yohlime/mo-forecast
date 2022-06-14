#!/usr/bin/env bash

#################### CONSTANTS ####################
DOWNLOAD_INPUT=1
DOWNLOAD_MADIS=1
UPLOAD_OUTPUT=1
POST_PROCESS=1
SLURM_OPTS0="--parsable -A $SLURM_ACCOUNT -p $SLURM_PARTITION -N $SLURM_NUM_NODES"
###################################################

#################### FUNCTIONS ####################
function show_usage() {
  printf "Usage: %s [options [parameters]]\n" "$0"
  printf "\n"
  printf "Options:\n"
  printf " --no-download, Do not download WRF inputs (GFS, etc...)\n"
  printf " --no-download-madis, Do not download 3DVAR inputs (MADIS, etc...)\n"
  printf " --no-upload, Do not upload outputs\n"
  printf " --no-post-proc, No post processing\n"
  printf " -h|--help, Print help\n"

  return 0
}
###################################################

################### PROCESS ARGS ###################
while [ -n "$1" ]; do
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

echo "-----------------------"
echo " Starting WRF Forecast "
echo "-----------------------"

# Cancel any previous slurm jobs
hn=`echo $HOSTNAME | cut -d . -f 1`
scancel --user=modelman --partition=${hn}

source "$SCRIPT_DIR/set_date_vars.sh"
MODEL_LOG_DIR="$LOG_DIR/model"
POST_LOG_DIR="$LOG_DIR/post"

mkdir -p "$MODEL_LOG_DIR"
mkdir -p "$POST_LOG_DIR"

if [ $DOWNLOAD_INPUT -eq 1 ]; then
  # download GFS
  source "$SCRIPT_DIR/download_gfs.sh"
fi

if [[ $WRF_MODE == '3dvar' && $DOWNLOAD_MADIS -eq 1 ]]; then
  # download MADIS
  source "$SCRIPT_DIR/download_madis.sh"
fi

GFS_FILES=("$GFS_DIR"/*.grb)
if [ ${#GFS_FILES[@]} -eq $NUM_FILES ]; then

  # WPS
  mkdir -p "$MODEL_LOG_DIR/wps"
  wps_log_file="$MODEL_LOG_DIR/wps/wps_$FCST_YYYYMMDD$FCST_ZZ.out"
  slurm_opts="$SLURM_OPTS0"
  slurm_opts="$slurm_opts -J wps-$FCST_YYYYMMDD$FCST_ZZ"
  slurm_opts="$slurm_opts -o $wps_log_file"
  slurm_opts="$slurm_opts -n $SLURM_WPS_NTASKS"
  prev_jid=$(sbatch $slurm_opts "$SCRIPT_DIR/run_wps.sh")

  # WRF
  # schedule multiple slurm WRF jobs based on WRF_RUN_NAMES
  IFS=':' read -ra run_names <<<"$WRF_RUN_NAMES"
  IFS=':' read -ra run3dvar_names <<<"$WRFDA_RUN_NAMES"
  run_idx=1
  for run_name in "${run_names[@]}"; do
    export NAMELIST_RUN=$run_name

    if [[ $WRF_MODE == '3dvar' ]]; then
      export NAMELIST_3DVar=${run3dvar_names[$run_idx - 1]}
    fi

    WRF_NTASKS=$SLURM_WRF_NTASKS
    mkdir -p "$MODEL_LOG_DIR/wrf"
    wrf_log_file="$MODEL_LOG_DIR/wrf/wrf_$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx}.out"
    slurm_opts="$SLURM_OPTS0"
    slurm_opts="$slurm_opts -d afterok:$prev_jid"
    slurm_opts="$slurm_opts -J wrf-$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx}"
    slurm_opts="$slurm_opts -o $wrf_log_file"
    slurm_opts="$slurm_opts -n $WRF_NTASKS"
    slurm_opts="$slurm_opts -c $SLURM_WRF_CPUS_PER_TASK"
    prev_jid=$(sbatch $slurm_opts "$SCRIPT_DIR/run_wrf.sh")

    run_idx=$((run_idx + 1))
  done

  if [ $POST_PROCESS -eq 1 ]; then
    # Post processing

    ### Python Post processing
    log_file="$POST_LOG_DIR/python_$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx}.log"
    slurm_opts="$SLURM_OPTS0"
    slurm_opts="$slurm_opts -d afterok:$prev_jid"
    slurm_opts="$slurm_opts -J python-$FCST_YYYYMMDD$FCST_ZZ"
    slurm_opts="$slurm_opts -o $log_file"
    slurm_opts="$slurm_opts -n 12"
    prev_jid=$(sbatch $slurm_opts "$SCRIPT_DIR/postproc_python.sh")

    if [ $UPLOAD_OUTPUT -eq 1 ]; then
      ### Web Upload
      mkdir -p "$POST_LOG_DIR/upload"
      log_file="$POST_LOG_DIR/upload/web-upload_$FCST_YYYYMMDD$FCST_ZZ.log"
      slurm_opts=$SLURM_OPTS0
      slurm_opts="$slurm_opts -d afterok:$prev_jid"
      slurm_opts="$slurm_opts -J web-upload-$FCST_YYYYMMDD$FCST_ZZ"
      slurm_opts="$slurm_opts -o $log_file"
      slurm_opts="$slurm_opts -n 1"
      prev_jid=$(sbatch $slurm_opts "$SCRIPT_DIR/web_upload.sh")
    fi

    ### ARWpost
    ### schedule multiple slurm ARWpost jobs based on WRF_RUN_NAMES
    IFS=':' read -ra run_names <<<"$WRF_RUN_NAMES"
    run_idx=1
    for run_name in "${run_names[@]}"; do
      export NAMELIST_RUN=$run_name

      mkdir -p "$POST_LOG_DIR/arw"
      arw_log_file="$POST_LOG_DIR/arw/arw_$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx}.out"
      slurm_opts=$SLURM_OPTS0
      slurm_opts="$slurm_opts -d afterok:$prev_jid"
      slurm_opts="$slurm_opts -J arw-$FCST_YYYYMMDD${FCST_ZZ}_run${run_idx}"
      slurm_opts="$slurm_opts -o $arw_log_file"
      slurm_opts="$slurm_opts -n 1"
      prev_jid=$(sbatch $slurm_opts "$SCRIPT_DIR/run_arwpost.sh")

      run_idx=$((run_idx + 1))
    done

    ### ENSEMBLE Post processing
    mkdir -p "$POST_LOG_DIR/ens"
    ens_log_file="$POST_LOG_DIR/ens/ens_$FCST_YYYYMMDD$FCST_ZZ.out"
    slurm_opts=$SLURM_OPTS0
    slurm_opts="$slurm_opts -d afterok:$prev_jid"
    slurm_opts="$slurm_opts -J ens-$FCST_YYYYMMDD$FCST_ZZ"
    slurm_opts="$slurm_opts -o $ens_log_file"
    slurm_opts="$slurm_opts -n 1"
    prev_jid=$(sbatch $slurm_opts "$SCRIPT_DIR/run_post_ens.sh")
  fi

fi
