#!/bin/bash

path=$(dirname "$0")

USER=ipf3-system
PASS=iY59RsDn

export http_proxy=http://proxy.olympus.co.jp:8080
export https_proxy=http://proxy.olympus.co.jp:8080

PROJECT_LIST=('CV2K製品' 'IPF-3 OTV製品' 'VE2製品試験' 'ツール' \
    '教育用testPJ' 'Sample_Env' 'OTV_SOMED_RTC' 'test_SOMED_RTC' 'sandbox_integ' 'Simulator')
#PROJECT_LIST=('CV2K製品')

for project in "${PROJECT_LIST[@]}"; do
    echo "${project}"_log
    python3 $path/insert_es.py --user $USER --password $PASS --project "$project" 2>&1 | tee /sync_log/"${project}"_log
done
