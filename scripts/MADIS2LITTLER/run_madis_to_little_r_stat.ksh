#! /bin/ksh -aeu

#######################################################################################
# Script: run_madis_to_little_r.ksh
#
# Purpose: To convert MADIS data into "little_r" format that OBSPROC uses
#
#  Input required: date and run directory information
#		Usage: madis_to_little_r.exe $ANALYSIS_DATE MADIS2LITTLE_R_DIR/
#		Format of required input: ANALYSIS_DATE=2007-04-23_18:00:00.0000
#       	MADIS2LITTLE_R_DIR=The path that you want to save little_r data
#
#
# Meral Demirtas, NCAR/DATC
# Ruifang Li: Added Canadian's SAO, SATWND 3h observation types.    10/19/2009
# Ruifang Li: Added mesoent type.                                   06/2010
# Ruifang Li: Added MAP, NPN, SATWND 1h observationi types.         03/2011
# Mike Kavulich: Updated for release                                10/2013
#######################################################################################

#######################################################
# It should not be necessary to edit beyond this line #
#######################################################

DATE=$MADIS_SDATE
while test "$DATE" -le "$MADIS_EDATE"; do

   # Define the working directory
   export WORKING_DIR=${MADIS2LITTLE_R_DIR}/${DATE}

   # Prepare sub-dirs for each obs types

   if [[ ! -d WORKING_DIR ]]; then
      if [[ (${METAR} = 'TRUE') ]]; then
         mkdir -p "${WORKING_DIR}/metar"
      fi

      if [[ (${ACARS} = 'TRUE') ]]; then
         mkdir -p "${WORKING_DIR}/acars"
      fi

      if [[ (${MARINE} = 'TRUE') ]]; then
         mkdir -p "${WORKING_DIR}/maritime"
      fi

      if [[ (${GPSPW} = 'TRUE') ]]; then
         mkdir -p "${WORKING_DIR}/gpspw"
      fi

      if [[ (${RAOB} = 'TRUE') ]]; then
         mkdir -p "${WORKING_DIR}/raob"
      fi

      if [[ (${SATWND} = 'TRUE') ]]; then
         mkdir -p "${WORKING_DIR}/HDW"
      fi

      if [[ (${NPN} = 'TRUE') ]]; then
         mkdir -p "${WORKING_DIR}/npn"
      fi

      if [[ (${MAP} = 'TRUE') ]]; then
         mkdir -p "${WORKING_DIR}/map"
      fi

   fi

   # Set input date required by the executable
   ANALYSIS_DATE=$("$MADIS_CODE_DIR/da_advance_time.exe" "$DATE" 0 -w).0000
   FILE_DATE="$(echo "$ANALYSIS_DATE" | cut -c1-13)"

   # Run the code
   if [[ (${METAR} = 'TRUE') || (${RAOB} = 'TRUE') || (${ACARS} = 'TRUE') || (${SATWND} = 'TRUE') ||
      (${MARINE} = 'TRUE') || (${NPN} = 'TRUE') || (${MAP} = 'TRUE') || (${GPSPW} = 'TRUE') ]]; then
      "$MADIS_CODE_DIR/madis_to_little_r.exe" "$ANALYSIS_DATE" "$WORKING_DIR/"
   else
      echo 'Please specify at least one obs to convert. EXIT ....'
      exit
   fi

   # Get the next date
   DATE=$("$MADIS_CODE_DIR/da_advance_time.exe" "$DATE" "$MADIS_INTERVAL")

done

echo 'MADIS2LITTLER complete!'
exit
