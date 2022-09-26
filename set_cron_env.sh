#!/bin/bash
. /etc/profile.d/rcs.sh
. $HOME/.bash_profile

export MAINDIR=$HOME/forecast

export TEMP_DIR=${MAINDIR}/.tmp
export SCRIPT_DIR=${MAINDIR}/scripts
export LOG_DIR=${MAINDIR}/logs

export GFS_BASE_DIR="${MAINDIR}/input/gfs_files"
export GFS_NC_DIR=${GFS_BASE_DIR}/nc
export MADIS_BASE_DIR="${MAINDIR}/input/madis_files"

export WPS_GFSDIR=${MAINDIR}/model/WPS/GFS
export WRF_MAINDIR=${MAINDIR}/model
export WRF_REALDIR=${MAINDIR}/model/WRF

export WRF_MODE=3dvar

export WRFRES=5
export WRF_FCST_DAYS=5
# export NAMELIST_SUFF=cmpXfcst25-5km
# export NAMELIST_SUFF=wcr_luzon
# export NAMELIST_SUFF=mowcr_D1
export NAMELIST_SUFF=mowcr_solar
export WPS_NAMELIST_SUFF=mowcr_solar
export WRF_RUN_NAMES=mowcr_solar_run1:mowcr_solar_run2:mowcr_solar_run3

# for WRFDA
export WRFDA_RUN_NAMES=3DVar_run1:3DVar_run2:3DVar_run3
export WINDOW_HOUR=3
export AWS_DIR=${MAINDIR}/input/aws_files
# end for WRFDA

export SLURM_WPS_NTASKS=6
export SLURM_WRF_NTASKS=96
#export SLURM_WRF_NTASKS=72
export SLURM_WRF_NTASKS2=96
hn=$(hostname -s)
export SLURM_PARTITION=$hn
export SLURM_NUM_NODES=1
export SLURM_ACCOUNT=rcs
export SLURM_USER=modelman
export SLURM_WRF_CPUS_PER_TASK=1

export OUTDIR=${MAINDIR}/output
export OUTDIR_LATEST_TIF=${OUTDIR}/tif/latest
export EWB_TIF=${MAINDIR}/ewb/tif
export EWB_TRMM_CLIM=${MAINDIR}/ewb/trmm/clim

export CDO=/opt/tools/nc/cdo

export CONDA_PREFIX=${MAINDIR}/venv
export MPLBACKEND="agg"
export PYTHONPATH=${SCRIPT_DIR}/python:${PYTHONPATH}
export PYTHON=${CONDA_PREFIX}/bin/python

#EWB
export EWB_DIR=${MAINDIR}/ewb_python
export GSMAP_NC_DIR=${MAINDIR}/input/gsmap
export GSMAP_DATA="gauge" # options : gauge , nrt , now [can only be run at 9:00 PHT sharp]
export CLIM_DIR=/home/modelman/forecast/climatology/frJulie/01_forForecasting
export APHRO_DIR=$CLIM_DIR/APHRODITE/rain/GRIDS_5km/MONTHLY
export TRMM_DIR=$CLIM_DIR/TRMM/GRIDS_5km/MONTHLY
export WRF_NC_DIR=${OUTDIR}/nc
