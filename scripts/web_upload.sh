#!/bin/bash

YY=${FCST_YYYYMMDD:0:4}
mm=${FCST_YYYYMMDD:4:2}
dd=${FCST_YYYYMMDD:6:2}

DATE2=$(date -d "$YY-$mm-${dd} $FCST_ZZ:00:00 8 hours" +'%Y-%m-%d %H:%M:%S')
read YY2 mm2 dd2 HH2 MM2 SS2 <<< ${DATE2//[-: ]/ }

echo "--------------------------"
echo " Uploading files for web  "
echo "--------------------------"

# SRCDIR=${OUTDIR}/.test
SRCDIR=${OUTDIR}

cat << EOF > ${SRCDIR}/info.json
{
    "year": "${YY2}",
    "month": "${mm2}", 
    "day": "${dd2}", 
    "hour": "${HH2}"
}
EOF
scp ${SRCDIR}/info.json panahon.linode:~/websites/panahon/resources/model/
scp ${SRCDIR}/info.json panahon.alapaap:~/websites/panahon-php/resources/model/

scp ${SRCDIR}/maps/wrf-*$YY2-$mm2-${dd2}_${HH2}PHT.png panahon.linode:~/websites/panahon/resources/model/img/
scp ${SRCDIR}/maps/wrf-*$YY2-$mm2-${dd2}_${HH2}PHT.png panahon.alapaap:~/websites/panahon-php/resources/model/img/

scp ${SRCDIR}/timeseries/img/wrf-*$YY2-$mm2-${dd2}_${HH2}PHT.png panahon.linode:~/websites/panahon/resources/model/img/
scp ${SRCDIR}/timeseries/img/wrf-*$YY2-$mm2-${dd2}_${HH2}PHT.png panahon.alapaap:~/websites/panahon-php/resources/model/img/

for f in $(find ${SRCDIR}/web/maps/ -type f -name "wrf-*$YY2-$mm2-${dd2}_${HH2}PHT.png"); do cp "$f" ${f%_$YY2-$mm2-${dd2}_${HH2}PHT.png}_latest.png; done
scp ${SRCDIR}/web/maps/*_latest.png panahon.linode:~/websites/panahon/resources/model/web_img/
scp ${SRCDIR}/web/maps/*_latest.png panahon.alapaap:~/websites/panahon-php/resources/model/web_img/

for f in $(find ${SRCDIR}/web/json/ -type f -name "forecast_*$YY2-$mm2-${dd2}_${HH2}PHT.json"); do cp "$f" ${f%_$YY2-$mm2-${dd2}_${HH2}PHT.json}_latest.json; done
scp ${SRCDIR}/web/json/forecast_latest.json panahon.linode:~/websites/panahon/resources/model/
scp ${SRCDIR}/web/json/forecast_latest.json panahon.alapaap:~/websites/panahon-php/resources/model/

echo "-----------------------------"
echo " Done uploading web files!!! "
echo "-----------------------------"

echo "--------------------------"
echo " Uploading files for ACEN  "
echo "--------------------------"

rclone copy ${SRCDIR}/acenergy/csv/acenergy_SACASOL_${YY2}-${mm2}-${dd2}_${HH2}PHT.csv ecw_acen:/ACEN/csv/
rclone copy ${SRCDIR}/acenergy/csv/acenergy_SOLARACE1_${YY2}-${mm2}-${dd2}_${HH2}PHT.csv ecw_acen:/ACEN/csv/
rclone copy ${SRCDIR}/acenergy/img/acenergy-ts_${YY2}-${mm2}-${dd2}_${HH2}PHT.png ecw_acen:/ACEN/img/

echo "-----------------------------"
echo " Done uploading ACEN files!!! "
echo "-----------------------------"
