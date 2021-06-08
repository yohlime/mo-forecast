#!/bin/bash

YY=${FCST_YYYYMMDD:0:4}
mm=${FCST_YYYYMMDD:4:2}
dd=${FCST_YYYYMMDD:6:2}

YY=(2021)
mm=(05)
dd=(20)
FCST_ZZ=(18)

DATE2=$(date -d "$YY-$mm-${dd} $FCST_ZZ:00:00 8 hours" +'%Y-%m-%d %H:%M:%S')
read YY2 mm2 dd2 HH2 MM2 SS2 <<< ${DATE2//[-: ]/ }

echo "------------------"
echo " Uploading files  "
echo "------------------"

mkdir -p ${MAINDIR}/output/latest
rm -f ${MAINDIR}/output/latest/*.png

find ${MAINDIR}/output/ -type f -name "wrf-*$YY2-$mm2-${dd2}_${HH2}PHT.png" -exec cp {} ${MAINDIR}/output/latest/ \;
#cp -p ${MAINDIR}/output/timeseries/img/forecast_MOD_$YY2-$mm2-${dd2}_${HH2}PHT.png ${MAINDIR}/output/latest/ts_forecast_$YY2-$mm2-${dd2}_${HH2}PHT.png
cp -p ${MAINDIR}/output/timeseries/img/forecast_$YY2-$mm2-${dd2}_${HH2}PHT.png ${MAINDIR}/output/latest/ts_forecast_$YY2-$mm2-${dd2}_${HH2}PHT.png
# rename _$YY2-$mm2-${dd2}_${HH2}PHT.png .png ${MAINDIR}/output/latest/*$YY2-$mm2-${dd2}_${HH2}PHT.png
for f in ${MAINDIR}/output/latest/*$YY2-$mm2-${dd2}_${HH2}PHT.png ; do mv -v "$f" ${f%_$YY2-$mm2-${dd2}_${HH2}PHT.png}.png; done

ssh panahon.linode "rm -f ~/websites/panahon/resources/model/img/*"
scp ${MAINDIR}/output/latest/*.png panahon.linode:~/websites/panahon/resources/model/img/


rm -f ${MAINDIR}/output/latest/info.json

cat > ${MAINDIR}/output/latest/info.json <<EOL
{
  "year": "$YY2",
  "month": "$mm2",
  "day": "$dd2",
  "hour": "$HH2"
}
EOL

scp ${MAINDIR}/output/latest/info.json panahon.linode:~/websites/panahon/resources/model/

echo "-------------------------"
echo " Done uploading files!!! "
echo "-------------------------"
