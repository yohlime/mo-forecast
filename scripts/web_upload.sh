#!/usr/bin/env bash

YY=${FCST_YYYYMMDD:0:4}
mm=${FCST_YYYYMMDD:4:2}
dd=${FCST_YYYYMMDD:6:2}

DATE2=$(date -d "$YY-$mm-$dd $FCST_ZZ:00:00 8 hours" +'%Y-%m-%d %H:%M:%S')
read -r YY2 mm2 dd2 HH2 MM2 SS2 <<<"${DATE2//[-: ]/ }"

echo "--------------------------"
echo " Uploading files for web  "
echo "--------------------------"

SRCDIR=${OUTDIR}

IMGS=("$SRCDIR/maps"/wrf-*"$YY2-$mm2-${dd2}_${HH2}PHT.png")
if [ ${#IMGS[@]} -eq 1 ]; then
  err_msg="No files to upload"
  echo "$err_msg" >>"$ERROR_FILE"
  echo "$err_msg"
  exit 1
fi

cat <<EOF >"$SRCDIR/info.json"
{
    "year": "$YY2",
    "month": "$mm2", 
    "day": "$dd2", 
    "hour": "$HH2"
}
EOF
scp "$SRCDIR/info.json" panahon.linode:~/websites/panahon/resources/model/
scp "$SRCDIR/info.json" panahon.alapaap:~/websites/panahon-php/resources/model/

# panahon.observatory.ph
scp "$SRCDIR/maps"/wrf-*"$YY2-$mm2-${dd2}_${HH2}PHT.png" panahon.linode:~/websites/panahon/resources/model/img/
scp "$SRCDIR/maps"/wrf-*"$YY2-$mm2-${dd2}_${HH2}PHT.png" panahon.alapaap:~/websites/panahon-php/resources/model/img/
scp "$SRCDIR/timeseries/img"/wrf-*"$YY2-$mm2-${dd2}_${HH2}PHT.png" panahon.linode:~/websites/panahon/resources/model/img/
scp "$SRCDIR/timeseries/img"/wrf-*"$YY2-$mm2-${dd2}_${HH2}PHT.png" panahon.alapaap:~/websites/panahon-php/resources/model/img/

# panahon.observatory.ph/ecw
scp "$SRCDIR/web/maps"/wrf-*"$YY2-$mm2-${dd2}_${HH2}PHT.png" panahon.linode:~/websites/panahon/resources/model/web_img/
scp "$SRCDIR/web/maps"/wrf-*"$YY2-$mm2-${dd2}_${HH2}PHT.png" panahon.alapaap:~/websites/panahon-php/resources/model/web_img/
scp "$SRCDIR/web/json/forecast_$YY2-$mm2-${dd2}_${HH2}PHT.json" panahon.linode:~/websites/panahon/resources/model/
scp "$SRCDIR/web/json/forecast_$YY2-$mm2-${dd2}_${HH2}PHT.json" panahon.alapaap:~/websites/panahon-php/resources/model/

echo "-----------------------------"
echo " Done uploading web files!!! "
echo "-----------------------------"

echo "--------------------------"
echo " Uploading files for EWB  "
echo "--------------------------"

scp -rp "$SRCDIR/web/maps/ewb/"*.png panahon.linode:~/websites/panahon/resources/model/img/ewb/
scp -rp "$SRCDIR/web/maps/ewb/"*.png panahon.alapaap:~/websites/panahon-php/resources/model/img/ewb/

echo "-----------------------------"
echo " Done uploading EWB files!!! "
echo "-----------------------------"

echo "--------------------------"
echo " Uploading files for EHB  "
echo "--------------------------"

rsubdir="ewb:EHB/resources/model/hi_gauge/$YY2$mm2$dd2/$HH2"
rclone copy "$SRCDIR/hi_gauge/img/$YY$mm$dd${FCST_ZZ}" "$rsubdir"

echo "-----------------------------"
echo " Done uploading EHB files!!! "
echo "-----------------------------"

echo "--------------------------"
echo " Uploading files for ACEN  "
echo "--------------------------"

rclone copy "$SRCDIR/acenergy/csv/acenergy_SACASOL_$YY2-$mm2-${dd2}_${HH2}PHT.csv" ecw_acen:/ACEN/csv/
rclone copy "$SRCDIR/acenergy/csv/acenergy_SOLARACE1_$YY2-$mm2-${dd2}_${HH2}PHT.csv" ecw_acen:/ACEN/csv/
rclone copy "$SRCDIR/acenergy/img/acenergy-ts_$YY2-$mm2-${dd2}_${HH2}PHT.png" ecw_acen:/ACEN/img/

echo "-----------------------------"
echo " Done uploading ACEN files!!! "
echo "-----------------------------"
