#!/bin/bash
. /etc/profile.d/rcs.sh
. $HOME/.bash_profile

export MAINDIR=$HOME/forecast

export TEMP_DIR=${MAINDIR}/.tmp
export SCRIPT_DIR=${MAINDIR}/scripts

export WRF_POSTDIR=${MAINDIR}/model/ARWpost
# export WRF_GFSDIR=${MAINDIR}/input/gfs_files
export WPS_GFSDIR=${MAINDIR}/model/WPS/GFS
export WRF_MAINDIR=${MAINDIR}/model
export WRF_REALDIR=${MAINDIR}/model/WRF

export WRFRES=5
export WRF_FCST_DAYS=3
# export NAMELIST_SUFF=cmpXfcst25-5km
# export NAMELIST_SUFF=wcr_luzon
# export NAMELIST_SUFF=mowcr_D1
export NAMELIST_SUFF=mowcr_solar

export SLURM_WPS_NTASKS=12
export SLURM_WRF_NTASKS=96
#export SLURM_WRF_NTASKS=72
export SLURM_WRF_NTASKS2=96
export SLURM_PARTITION=dugong
export SLURM_NUM_NODES=1
export SLURM_ACCOUNT=rcs

export OUTDIR=${MAINDIR}/output
export OUTDIR_LATEST_TIF=${OUTDIR}/tif/latest
export EWB_TIF=${MAINDIR}/ewb/tif
export EWB_TRMM_CLIM=${MAINDIR}/ewb/trmm/clim

export CDO=/home/miniconda3/envs/toolbox/bin/cdo

export CONDA_TOOLBOX=toolbox
export CONDA_QGIS=qgis

export QGIS_PREFIX_PATH=/home/miniconda3/envs/qgis
#export PYTHONPATH=${QGIS_PREFIX_PATH}/share/qgis/python/plugins:${QGIS_PREFIX_PATH}/share/qgis/python:${QGIS_PREFIX_PATH}/share/qgis/python/plugins/processing:${QGIS_PREFIX_PATH}/share/qgis/python:${HOME}/.qgis2/python:${HOME}/.qgis2/python/plugins:${QGIS_PREFIX_PATH}/share/qgis/python/plugins:$PYTHONPATH
export PYTHONPATH=${QGIS_PREFIX_PATH}/share/qgis/python/plugins:${QGIS_PREFIX_PATH}/share/qgis/python:${QGIS_PREFIX_PATH}/lib/python3.9/site-packages:$PYTHONPATH
export LD_LIBRARY_PATH=${QGIS_PREFIX_PATH}/lib:${QGIS_PREFIX_PATH}/lib/python3.9/site-packages/PyQt5:$LD_LIBRARY_PATH
export QT_PLUGIN_PATH=${QGIS_PREFIX_PATH}/plugins:$QT_PLUGIN_PATH
export PROJ_LIB=${QGIS_PREFIX_PATH}/share/proj
export PROJ_NETWORK=ON
export GDAL_DATA=${QGIS_PREFIX_PATH}/share/gdal
export GSETTINGS_SCHEMA_DIR=${QGIS_PREFIX_PATH}/share/glib-2.0/schemas

