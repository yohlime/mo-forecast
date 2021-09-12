#!/bin/bash

DATA=${GSMAP_DATA}
CDO=/home/miniconda3/envs/toolbox/bin/cdo
GSMAPDIR=$MAINDIR/validation/gsmap

cd $GSMAPDIR

# Make ctl file
DATE_STR1=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} $FCST_ZZ:00:00" +'%Y-%b-%d_%H')
read FCST_YY_Z FCST_MM_Z FCST_DD_Z FCST_HH_Z <<< ${DATE_STR1//[-_]/ }

sed -i "16s/.*/TDEF   24 LINEAR ${FCST_ZZ}Z${FCST_DD}${FCST_MM_Z}${FCST_YY} 1hr/" gsmap_${DATA}.ctl
rm -f gsmap_${DATA}_*.ctl
ln -s gsmap_${DATA}.ctl gsmap_${DATA}_${FCST_YY}-${FCST_MM}-${FCST_DD}_$FCST_ZZ.ctl

# Converting to netCDF
echo "start ${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}"
echo "Converting to netCDF..."
$CDO -f nc import_binary gsmap_${DATA}_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}.ctl gsmap_${DATA}_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}.nc
echo "Trimming netCDF to PH domain..."
$CDO sellonlatbox,115,129,4.8,21 gsmap_${DATA}_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}.nc nc/gsmap_${DATA}_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}_ph.nc
$CDO daysum nc/gsmap_${DATA}_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}_ph.nc nc/gsmap_${DATA}_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}.nc
rm gsmap_${DATA}_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}.nc
echo "done! ${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}"