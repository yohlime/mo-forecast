#!/bin/bash

# -------------------------------------------- #
#     Process MADIS+ AWS assimilation data     #
# -------------------------------------------- #
echo "  *************************  "
echo " Preparing assimilation data "
echo "  *************************  "
# assimilation window (how many hours before and after the initialization time)
SDAT=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} ${FCST_ZZ}:00:00 $((WINDOW_HOUR)) hours ago" +'%Y-%m-%d %H:%M:%S')
YYS=${SDAT:0:4}
MMS=${SDAT:5:2}
DDS=${SDAT:8:2}
HHS=${SDAT:11:2}
EDAT=$(date -d "${FCST_YY}-${FCST_MM}-${FCST_DD} ${FCST_ZZ}:00:00 $((WINDOW_HOUR)) hours" +'%Y-%m-%d %H:%M:%S')
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

#mkdir -p ${MAINDIR}/input/madis_files/MADIS2LITTLER/point
cd "$SCRIPT_DIR/MADIS2LITTLER" || exit
rm -rf "$MAINDIR"/input/madis_files/MADIS2LITTLER/point/*
ln -s "$MADIS_DIR"/* "$MAINDIR"/input/madis_files/MADIS2LITTLER/point/.

# Edit madis_to_little_r.ksh
rm -f run_madis_to_little_r.ksh
sed -i "5s~.*~export MADIS_DATA=${MAINDIR}/input/madis_files/MADIS2LITTLER~" .env
sed -i "6s~.*~export MADIS_STATIC=/home/MODELS/WRFutils/madis-4.3/static/~" .env
sed -i "15s/.*/export METAR=TRUE/" .env
sed -i "16s/.*/export MARINE=TRUE/" .env
sed -i "17s/.*/export GPSPW=FALSE/" .env
sed -i "18s/.*/export ACARS=TRUE/" .env
sed -i "19s/.*/export RAOB=TRUE/" .env
sed -i "20s/.*/export NPN=FALSE/" .env
sed -i "21s/.*/export MAP=FALSE/" .env
sed -i "22s/.*/export SATWND=TRUE/" .env
sed -i "26s/.*/export MADIS_SDATE=$YYS$MMS$DDS$HHS/" .env
sed -i "27s/.*/export MADIS_EDATE=$YYE$MME$DDE$HHE/" .env
sed -i "28s/.*/export MADIS_INTERVAL=1/" .env
sed -i "33s~.*~export MADIS_CODE_DIR=${SCRIPT_DIR}/MADIS2LITTLER/~" .env
ln -s run_madis_to_little_r_stat.ksh run_madis_to_little_r.ksh

source ./.env
./run_madis_to_little_r.ksh >&log.madistolittler &
tail --pid=$! -f log.madistolittler
mv log.madistolittler "$MAINDIR"/input/madis_files/MADIS2LITTLER/.

echo "End of madis to little r!"
echo " *********************** "

echo " ************************** "
echo "Converting AWS to little r..."

#mkdir -p ${MAINDIR}/input/aws_files/point
cd "$SCRIPT_DIR/MO2LITTLER" || exit
rm -rf "$MAINDIR"/input/aws_files/MO2LITTLER/point/*
rm "$SCRIPT_DIR"/MO2LITTLER/*.csv

# Edit prepare_stations.py
sed -i "1s~.*~export IN_DIR='${AWS_DIR}'~" .env
# sed -i "8s~.*~WORK_DIR = '${WRF_MAINDIR}/MO2LITTLER'~" prepare_stations.py
sed -i "2s~.*~export OUT_DIR='${MAINDIR}/input/aws_files/MO2LITTLER/point'~" .env
sed -i "3s/.*/export YYYYMMDD='${YYA}-${MMA}-${DDA}'/" .env
sed -i "4s/.*/export HH_INIT='${HHA}PHT'/" .env

echo " ************************** "
echo "Preparing station data..."
$PYTHON prepare_stations.py

ln -s "$MAINDIR"/input/aws_files/MO2LITTLER/point/*.csv .
ln -s "$MAINDIR"/input/aws_files/MO2LITTLER/coordinates_data.csv .

./convert.exe

mkdir -p "$MAINDIR/input/aws_files/MO2LITTLER/little_r_obs/$YYS$MMS$DDS$HHS"
mv obs_MOstns_r* "$MAINDIR/input/aws_files/MO2LITTLER/little_r_obs/$YYS$MMS$DDS$HHS"

echo "End of aws to little r!"
echo " *********************** "

# Combine converted AWS data per hour
DIRAWS="$MAINDIR/input/aws_files/MO2LITTLER/little_r_obs/$YYS$MMS$DDS$HHS"
cd "$DIRAWS" || exit
AWS_LIST=("")
CDAT=$SDAT
while [ "$CDAT" != "$TDAT" ]; do
  YY=${CDAT:0:4}
  MM=${CDAT:5:2}
  DD=${CDAT:8:2}
  HH=${CDAT:11:2}
  AWS_LIST=(${AWS_LIST[@]} "obs_MOstns_r_$YY-$MM-${DD}_${HH}")
  CDAT=$(date -d "$CDAT 1 hour" +'%Y-%m-%d %H:%M:%S')
done

# Combine converted MADIS data per hour
cd "$MAINDIR/input/madis_files/MADIS2LITTLER/little_r_obs" || exit
MADIS_LIST=("")
CDAT=$SDAT
while [ "$CDAT" != "$TDAT" ]; do
  YY=${CDAT:0:4}
  MM=${CDAT:5:2}
  DD=${CDAT:8:2}
  HH=${CDAT:11:2}
  cat "$YY$MM$DD$HH"/*/* >"obs_$YY$MM$DD$HH"
  MADIS_LIST=(${MADIS_LIST[@]} "obs_$YY$MM$DD$HH")
  CDAT=$(date -d "$CDAT 1 hour" +'%Y-%m-%d %H:%M:%S')
done

# Combine MADIS and AWS data per hour
FILE_LIST=("")
COUNT=0
while [ "$COUNT" != 7 ]; do
  cat ${MADIS_LIST[${COUNT}]} $DIRAWS/${AWS_LIST[${COUNT}]} >obsall_${COUNT}
  FILE_LIST=(${FILE_LIST[@]} "obsall_${COUNT}")
  COUNT=$((COUNT + 1))
done

# Create master assimilation data file (.ascii)
echo "concatenating : " ${FILE_LIST[*]}
cat $(echo ${FILE_LIST[*]}) >"ob_$YYS$MMS$DDS${HHS}.ascii"

# Cleanup files and remove redundant observation data for assimilation to free storage space
rm -rf "$MAINDIR/input/aws_files/MO2LITTLER/little_r_obs/$YYS$MMS$DDS$HHS" # MADIS data from individual sources
rm "$MAINDIR"/input/aws_files/MO2LITTLER/little_r_obs/obs_*                # concatenated MADIS data
rm "$MAINDIR"/input/aws_files/MO2LITTLER/little_r_obs/obsall_*             # concatenated MADIS + AWS data

# -------------------------------------------- #
#                 Run OBSPROC                  #
# -------------------------------------------- #
cd "$WRF_MAINDIR/WRF3DVar/OBSPROC" || exit
rm "ob_$YYS$MMS$DDS${HHS}.ascii"
ln -s "$MAINDIR/input/madis_files/MADIS2LITTLER/little_r_obs/ob_$YYS$MMS$DDS${HHS}.ascii" .

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
./obsproc.exe >&log.obsproc &
tail --pid=$! -f log.obsproc
echo "End of obsproc.exe!"
echo " *********************** "
# -------------------------------------------- #
#                 Run WRFDA                    #
# -------------------------------------------- #
echo "  ********************  "
echo " Running WRFDA "
echo "  ********************  "

cd "$WRF_MAINDIR/WRF3DVar" || exit
rm -f fg wrfbdy_d01 wrfinput_d01 ob.ascii
ln -s "$WRF_REALDIR/wrfreal_tmp/wrfinput_d01_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}" fg
ln -s "$WRF_REALDIR/wrfreal_tmp/wrfbdy_d01_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}" wrfbdy_d01
ln -s "$WRF_MAINDIR/WRF3DVar/OBSPROC/obs_gts_${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}:00:00.3DVAR" ob.ascii

# Edit namelist.input (WRFDA)
rm -f namelist.input
sed -i "45s/.*/analysis_date=\"${FCST_YY}-${FCST_MM}-${FCST_DD}_${FCST_ZZ}:00:00.0000\",/" "namelist.input_$NAMELIST_3DVar"
sed -i "52s/.*/time_window_min=\"${YYS}-${MMS}-${DDS}_${HHS}:00:00.0000\",/" "namelist.input_$NAMELIST_3DVar"
sed -i "55s/.*/time_window_max=\"${YYE}-${MME}-${DDE}_${HHE}:00:00.0000\",/" "namelist.input_$NAMELIST_3DVar"
sed -i "58s/.*/start_year=${FCST_YY},/" "namelist.input_$NAMELIST_3DVar"
sed -i "59s/.*/start_month=${FCST_MM},/" "namelist.input_$NAMELIST_3DVar"
sed -i "60s/.*/start_day=${FCST_DD},/" "namelist.input_$NAMELIST_3DVar"
sed -i "61s/.*/start_hour=${FCST_ZZ},/" "namelist.input_$NAMELIST_3DVar"
sed -i "62s/.*/end_year=${FCST_YY2},/" "namelist.input_$NAMELIST_3DVar"
sed -i "63s/.*/end_month=${FCST_MM2},/" "namelist.input_$NAMELIST_3DVar"
sed -i "64s/.*/end_day=${FCST_DD2},/" "namelist.input_$NAMELIST_3DVar"
sed -i "65s/.*/end_hour=${FCST_ZZ2},/" "namelist.input_$NAMELIST_3DVar"
ln -s "namelist.input_$NAMELIST_3DVar" namelist.input

# Run WRF-3DVar
echo " *********************** "
echo "Running da_wrfvar..."
# ./da_wrfvar.exe >& log.wrfda & tail --pid=$! -f log.wrfda
srun ./da_wrfvar.exe >&log.wrfda &
tail --pid=$! -f rsl.error.0000
echo "End of da_wrfvar!"
echo " *********************** "

# Update lateral boundary conditions
echo " *********************** "
echo "Running da_update_bc..."
srun ./da_update_bc.exe >&log.bcupdate &
tail --pid=$! -f rsl.error.0000
echo "End of da_update_bc!"
echo " *********************** "

mv wrfvar_output wrfinput_d01

echo "  ********************  "
echo " End of WRFDA "
echo "  ********************  "
