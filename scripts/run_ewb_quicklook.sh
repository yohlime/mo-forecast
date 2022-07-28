#!/bin/bash

cd "$SCRIPT_DIR/python" || exit
${PYTHON} ewb_total_precip_stations.py
${PYTHON} ewb_total_precip_gsmap.py
cd "$MAINDIR" || exit
