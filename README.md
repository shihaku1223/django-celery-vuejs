## Command

```bash
$ ./app.py [--text <text phrase>] \
  [--id <mantis ticket id>] \
  --csvs <mantis csv file path> [--csvs <mantis csv file path>] \
  --column <計算する対象カラム> (default '要約') \
  [--nums <結果表示数> (defaut 130)] \
  [--show-id]
```

## Example
### テキストのフレーズで検索を行う
```bash
$ ./app.py --text 'ユーザー設定画面を操作中に、モダコン の接続が切れて' \
  --csvs OTV_App.csv --csvs CV2K_App.csv \
  --column '詳細' \
  --nums 10
```

### 入力したIDに該当するチケットの内容で検索を行う
```bash
$ ./app.py --id 47934 \
  --csvs OTV_App.csv --csvs CV2K_App.csv \
  --column '詳細' \
  --nums 20
```

### 指定されたcsvファイルにあるチケットidを表示する
```bash
$ ./app.py --show-id
  --csvs OTV_App.csv --csvs CV2K_App.csv
```

## Build Docker image
```
$ docker build -t simapp .
```

## Using Docker image to calculate similarity

run.shを参照ください。

```
$ docker run --rm \
  --name simapp \
  -v $(pwd)/csvs:/csvs \
  -v $(pwd)/tfhub_modules:/tmp/tfhub_modules \
  -it simapp \
  --text 'ユーザー設定画面を操作中に、モダコン の接続が切れて' \
  --csvs /csvs/CV2K_App.csv  \
  --column '詳細'
```
