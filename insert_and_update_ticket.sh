#!/bin/bash

USER=10079186
PASS=!vp5QmS1223

PROJECT_LIST=('CV2K製品' 'IPF-3 OTV製品' 'VE2製品試験' 'ツール' \
    '教育用testPJ' 'Sample_Env' 'TEST' 'test_SOMED_RTC' 'sandbox_integ' 'Simulator')

for project in "${PROJECT_LIST[@]}"; do
    echo $project
    python3 insert.py --user $USER --password $PASS --project $project
    python3 calc.py --project $project
done
