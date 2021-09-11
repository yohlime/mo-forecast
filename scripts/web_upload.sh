#!/bin/bash

YY=${FCST_YYYYMMDD:0:4}
mm=${FCST_YYYYMMDD:4:2}
dd=${FCST_YYYYMMDD:6:2}

DATE2=$(date -d "$YY-$mm-${dd} $FCST_ZZ:00:00 8 hours" +'%Y-%m-%d %H:%M:%S')
read YY2 mm2 dd2 HH2 MM2 SS2 <<< ${DATE2//[-: ]/ }

echo "--------------------------"
echo " Uploading files for web  "
echo "--------------------------"

for f in $(find ${MAINDIR}/output/.test/web/maps/ -type f -name "wrf-*$YY2-$mm2-${dd2}_${HH2}PHT.png"); do cp "$f" ${f%_$YY2-$mm2-${dd2}_${HH2}PHT.png}_latest.png; done
scp ${MAINDIR}/output/.test/web/maps/*_latest.png panahon.linode:~/websites/panahon/resources/model/web_img/
scp ${MAINDIR}/output/.test/web/maps/*_latest.png panahon.alapaap:~/websites/panahon-php/resources/model/web_img/

for f in $(find ${MAINDIR}/output/.test/web/json/ -type f -name "forecast_*$YY2-$mm2-${dd2}_${HH2}PHT.json"); do cp "$f" ${f%_$YY2-$mm2-${dd2}_${HH2}PHT.json}_latest.json; done
scp ${MAINDIR}/output/.test/web/json/forecast_latest.json panahon.linode:~/websites/panahon/resources/model/
scp ${MAINDIR}/output/.test/web/json/forecast_latest.json panahon.alapaap:~/websites/panahon-php/resources/model/

echo "-----------------------------"
echo " Done uploading web files!!! "
echo "-----------------------------"
