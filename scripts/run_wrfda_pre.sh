#!/bin/bash

# -------------------------------------------- #
#     Process MADIS+ AWS assimilation data     #
# -------------------------------------------- #
echo "  *************************  "
echo " Preparing assimilation data "
echo "  *************************  "
# assimilation window (how many hours before and after the initialization time)
SDAT=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} ${FCST_ZZ}:00:00 $((${WINDOW_HOUR})) hours ago" +'%Y-%m-%d %H:%M:%S')
YYS=${SDAT:0:4}
MMS=${SDAT:5:2}
DDS=${SDAT:8:2}
HHS=${SDAT:11:2}
EDAT=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} ${FCST_ZZ}:00:00 $((${WINDOW_HOUR})) hours" +'%Y-%m-%d %H:%M:%S')
YYE=${EDAT:0:4}
MME=${EDAT:5:2}
DDE=${EDAT:8:2}
HHE=${EDAT:11:2}
TDAT=$(date -d "$EDAT 1 hours" +'%Y-%m-%d %H:%M:%S')
# AWS data to start 11 hours ago
AWSDAT=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} ${FCST_ZZ}:00:00 11 hours ago" +'%Y-%m-%d %H:%M:%S')
YYA=${AWSDAT:0:4}
MMA=${AWSDAT:5:2}
DDA=${AWSDAT:8:2}
HHA=${AWSDAT:11:2}

echo " ************************** "
echo "Running madis_to_little_r..."

#mkdir -p ${WRF_MAINDIR}/MADIS2LITTLER/input/point
cd ${WRF_MAINDIR}/MADIS2LITTLER
rm -rf ${WRF_MAINDIR}/MADIS2LITTLER/input/point/*
ln -s ${MADISDIR}/* ${WRF_MAINDIR}/MADIS2LITTLER/input/point/.

# Edit madis_to_little_r.ksh
rm -f run_madis_to_little_r.ksh
sed -i "26s~.*~export MADIS_DATA=${WRF_MAINDIR}/MADIS2LITTLER/input~" run_madis_to_little_r_stat.ksh
sed -i "27s~.*~export MADIS_STATIC=/home/MODELS/WRFutils/madis-4.3/static/~" run_madis_to_little_r_stat.ksh
sed -i "37s/.*/export METAR=TRUE/" run_madis_to_little_r_stat.ksh
sed -i "38s/.*/export MARINE=TRUE/" run_madis_to_little_r_stat.ksh
sed -i "39s/.*/export GPSPW=FALSE/" run_madis_to_little_r_stat.ksh
sed -i "40s/.*/export ACARS=TRUE/" run_madis_to_little_r_stat.ksh
sed -i "41s/.*/export RAOB=TRUE/" run_madis_to_little_r_stat.ksh
sed -i "42s/.*/export NPN=FALSE/" run_madis_to_little_r_stat.ksh
sed -i "43s/.*/export MAP=FALSE/" run_madis_to_little_r_stat.ksh
sed -i "44s/.*/export SATWND=TRUE/" run_madis_to_little_r_stat.ksh
sed -i "49s/.*/SDATE=$YYS$MMS$DDS$HHS/" run_madis_to_little_r_stat.ksh
sed -i "50s/.*/EDATE=$YYE$MME$DDE$HHE/" run_madis_to_little_r_stat.ksh
sed -i "51s/.*/INTERVAL=1/" run_madis_to_little_r_stat.ksh
ln -s run_madis_to_little_r_stat.ksh run_madis_to_little_r.ksh


./run_madis_to_little_r.ksh >& log.madistolittler & tail --pid=$! -f log.madistolittler

echo "End of madis to little r!"
echo " *********************** "

echo " ************************** "
echo "Converting AWS to little r..."

#mkdir -p ${WRF_MAINDIR}/MO2LITTLER/input/point
cd ${WRF_MAINDIR}/MO2LITTLER
rm -rf ${WRF_MAINDIR}/MO2LITTLER/input/point/*
rm ${WRF_MAINDIR}/MO2LITTLER/*.csv

# Edit prepare_stations.py
sed -i "7s~.*~IN_DIR  = '${AWSDIR}'~" prepare_stations.py
sed -i "8s~.*~WORK_DIR = '${WRF_MAINDIR}/MO2LITTLER'~" prepare_stations.py
sed -i "9s~.*~OUT_DIR = '${WRF_MAINDIR}/MO2LITTLER/input/point'~" prepare_stations.py
sed -i "10s/.*/yyyymmdd = '${YYA}-${MMA}-${DDA}'/" prepare_stations.py
sed -i "11s/.*/init = '${HHA}PHT'/" prepare_stations.py

echo " ************************** "
echo "Preparing station data..."
$PYTHON prepare_stations.py

ln -s input/point/*.csv .
ln -s ${AWSDIR}/coordinates.csv .

./convert.exe

mkdir -p input/little_r_obs/$YYS$MMS$DDS$HHS
mv obs_MOstns_r* input/little_r_obs/$YYS$MMS$DDS$HHS

echo "End of aws to little r!"
echo " *********************** "

# Combine converted AWS data per hour
DIRAWS=${WRF_MAINDIR}/MO2LITTLER/input/little_r_obs/$YYS$MMS$DDS$HHS
cd $DIRAWS
AWS_LIST=("")
CDAT=$SDAT
while [ "$CDAT" != "$TDAT" ]
do
  YY=${CDAT:0:4}
  MM=${CDAT:5:2}
  DD=${CDAT:8:2}
  HH=${CDAT:11:2}
  AWS_LIST=(${AWS_LIST[@]} "obs_MOstns_r_$YY-$MM-${DD}_${HH}")
  CDAT=$(date -d "$CDAT 1 hour" +'%Y-%m-%d %H:%M:%S')
done

# Combine converted MADIS data per hour
cd ${WRF_MAINDIR}/MADIS2LITTLER/input/little_r_obs
MADIS_LIST=("")
CDAT=$SDAT
while [ "$CDAT" != "$TDAT" ]
do
  YY=${CDAT:0:4}
  MM=${CDAT:5:2}
  DD=${CDAT:8:2}
  HH=${CDAT:11:2}
  cat $YY$MM$DD$HH/*/* > obs_$YY$MM$DD$HH
  MADIS_LIST=(${MADIS_LIST[@]} "obs_$YY$MM$DD$HH")
  CDAT=$(date -d "$CDAT 1 hour" +'%Y-%m-%d %H:%M:%S')
done

# Combine MADIS and AWS data per hour
FILE_LIST=("")
COUNT=0
while [ "$COUNT" != 7 ]
do
  cat ${MADIS_LIST[${COUNT}]} $DIRAWS/${AWS_LIST[${COUNT}]} > obsall_${COUNT}
  FILE_LIST=(${FILE_LIST[@]} "obsall_${COUNT}")
  COUNT=$(( $COUNT + 1 ))
done

# Create master assimilation data file (.ascii)
echo "concatenating : " ${FILE_LIST[*]}
cat $(echo ${FILE_LIST[*]}) > ob_$YYS$MMS$DDS${HHS}.ascii

# -------------------------------------------- #
#                 Run OBSPROC                  #
# -------------------------------------------- #
cd ${WRF_MAINDIR}/WRF3DVar/OBSPROC
rm ob_$YYS$MMS$DDS${HHS}.ascii
ln -s ${WRF_MAINDIR}/MADIS2LITTLER/input/little_r_obs/ob_$YYS$MMS$DDS${HHS}.ascii .

# Edit namelist.obsproc
rm -f namelist.obsproc
sed -i "2s/.*/ obs_gts_filename = 'ob_$YYS$MMS$DDS${HHS}.ascii',/" namelist.obsproc_3DVar
sed -i "3s/.*/ obs_err_filename = 'obserr.txt',/" namelist.obsproc_3DVar
sed -i "9s/.*/ time_window_min  = '${YYS}-${MMS}-${DDS}_${HHS}:00:00',/" namelist.obsproc_3DVar
sed -i "10s/.*/ time_analysis    = '${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}:00:00',/" namelist.obsproc_3DVar
sed -i "11s/.*/ time_window_max  = '${YYE}-${MME}-${DDE}_${HHE}:00:00',/" namelist.obsproc_3DVar
sed -i "79s/.*/ NUM_SLOTS_PAST  =           ${WINDOW_HOUR},/" namelist.obsproc_3DVar
sed -i "80s/.*/ NUM_SLOTS_AHEAD =           ${WINDOW_HOUR},/" namelist.obsproc_3DVar
ln -s namelist.obsproc_3DVar namelist.obsproc

rm -f obs_* UV.txt HEIGHT.txt SPD.txt DIR.txt TEMP.txt RH.txt PRES.txt 

echo " *********************** "
echo "Running obsproc.exe..."
./obsproc.exe >& log.obsproc & tail --pid=$! -f log.obsproc
echo "End of obsproc.exe!"
echo " *********************** "
# -------------------------------------------- #
#                 Run WRFDA                    #
# -------------------------------------------- #
echo "  ********************  "
echo " Running WRFDA "
echo "  ********************  "

cd ${WRF_MAINDIR}/WRF3DVar
rm -f fg wrfbdy_d01 wrfinput_d01 ob.ascii 
ln -s ${WRF_REALDIR}/wrfreal_tmp/wrfinput_d01_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ} fg
ln -s ${WRF_REALDIR}/wrfreal_tmp/wrfbdy_d01_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ} wrfbdy_d01
ln -s ${WRF_MAINDIR}/WRF3DVar/OBSPROC/obs_gts_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}:00:00.3DVAR ob.ascii

# Edit namelist.input (WRFDA)
rm -f namelist.input
sed -i "45s/.*/analysis_date=\"${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}:00:00.0000\",/" namelist.input_${NAMELIST_3DVar}
sed -i "52s/.*/time_window_min=\"${YYS}-${MMS}-${DDS}_${HHS}:00:00.0000\",/" namelist.input_${NAMELIST_3DVar}
sed -i "55s/.*/time_window_max=\"${YYE}-${MME}-${DDE}_${HHE}:00:00.0000\",/" namelist.input_${NAMELIST_3DVar}
sed -i "58s/.*/start_year=${FCST_YY},/" namelist.input_${NAMELIST_3DVar}
sed -i "59s/.*/start_month=${FCST_MM},/" namelist.input_${NAMELIST_3DVar}
sed -i "60s/.*/start_day=${FCST_DD},/" namelist.input_${NAMELIST_3DVar}
sed -i "61s/.*/start_hour=${FCST_ZZ},/" namelist.input_${NAMELIST_3DVar}
sed -i "62s/.*/end_year=${FCST_YY2},/" namelist.input_${NAMELIST_3DVar}
sed -i "63s/.*/end_month=${FCST_MM2},/" namelist.input_${NAMELIST_3DVar}
sed -i "64s/.*/end_day=${FCST_DD2},/" namelist.input_${NAMELIST_3DVar}
sed -i "65s/.*/end_hour=${FCST_ZZ2},/" namelist.input_${NAMELIST_3DVar}
ln -s namelist.input_${NAMELIST_3DVar} namelist.input

# Run WRF-3DVar
echo " *********************** "
echo "Running da_wrfvar..."
# ./da_wrfvar.exe >& log.wrfda & tail --pid=$! -f log.wrfda
srun ./da_wrfvar.exe >& log.wrfda & tail --pid=$! -f rsl.error.0000
echo "End of da_wrfvar!"
echo " *********************** "

# Update lateral boundary conditions
echo " *********************** "
echo "Running da_update_bc..."
srun ./da_update_bc.exe >& log.bcupdate & tail --pid=$! -f rsl.error.0000
echo "End of da_update_bc!"
echo " *********************** "

mv wrfvar_output wrfinput_d01

echo "  ********************  "
echo " End of WRFDA "
echo "  ********************  "
