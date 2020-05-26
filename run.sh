#!/bin/bash

docker run --rm \
  --name simapp \
  -v $(pwd)/csvs:/csvs \
  -v $(pwd)/tfhub_modules:/tmp/tfhub_modules \
  -it simapp \
  --text 'ユーザー設定画面を操作中に、モダコン の接続が切れて' \
  --csvs /csvs/CV2K_App.csv  \
  --column '詳細'
