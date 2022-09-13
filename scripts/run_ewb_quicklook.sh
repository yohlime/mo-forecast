#!/bin/bash

cd "$MAINDIR/scripts" || exit

FILE=$(find "${GSMAP_NC_DIR}"/*"${FCST_YY_GSMAP}"-"${FCST_MM_GSMAP}"-"${FCST_DD_GSMAP}"_"${FCST_ZZ_GSMAP}"* | head -1)

if [ ! -f "$FILE" ]; then

  mkdir -p "$GSMAP_TEMP_DIR"
  # Download GSMaP data
  ./download_gsmap.sh
  # Convert GSMaP .gz files to .nc
  cd "$SCRIPT_DIR/python" || exit
  $PYTHON convert_gsmap_nc.py -i "$GSMAP_TEMP_DIR" -o "$GSMAP_NC_DIR"
  # Remove .gz files
  rm -rf "${GSMAP_TEMP_DIR?:}"
fi

$PYTHON ewb_total_precip_stations.py
$PYTHON ewb_total_precip_gsmap.py

echo "--------------------------"
echo " Uploading files for EWB  "
echo "--------------------------"

web_dirs=("panahon.alapaap:websites/panahon-php" "panahon.linode:websites/panahon-php")

for web_dir in "${web_dirs[@]}"; do
  scp -rp "${OUTDIR}/web/maps/ewb/"*.png "${web_dir}/resources/model/img/ewb/"
done

echo "-----------------------------"
echo " Done uploading EWB files!!! "
echo "-----------------------------"

cd "$MAINDIR" || exit
