#!/bin/bash

cd "$SCRIPT_DIR/python" || exit
${PYTHON} plot_7day_precip_stations.py
cd "$MAINDIR" || exit