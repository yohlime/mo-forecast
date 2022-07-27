#!/bin/bash

cd "$SCRIPT_DIR/python" || exit
${PYTHON} plot_total_precip_stations.py
cd "$MAINDIR" || exit
