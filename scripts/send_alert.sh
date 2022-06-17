#!/bin/bash

cd "$SCRIPT_DIR/python" || exit
${PYTHON} send_alert.py
cd "$MAINDIR" || exit
