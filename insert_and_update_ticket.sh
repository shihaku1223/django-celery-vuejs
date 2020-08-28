#!/bin/bash

path=$(dirname "$0")

USER=ipf3-system
PASS=iY59RsDn

export http_proxy=http://proxy.olympus.co.jp:8080
export https_proxy=http://proxy.olympus.co.jp:8080

PROJECT_LIST=('CV2K製品' 'IPF-3 OTV製品' 'VE2製品試験' 'ツール' \
    '教育用testPJ' 'Sample_Env' 'TEST' 'test_SOMED_RTC' 'sandbox_integ' 'Simulator')
#PROJECT_LIST=('sandbox_integ')

for project in "${PROJECT_LIST[@]}"; do
    echo $project
    python3 $path/insert.py --user $USER --password $PASS --project "$project"
    python3 $path/calc.py --project "$project"
done
