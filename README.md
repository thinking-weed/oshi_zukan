# object_detection_app（推し図鑑（自分の推しの画像収集図鑑）・画像検知アプリ）

git clone後以下のコマンドで動くはず・・・（Pythonのversionは3.9.6を使用しています）

<h3>powershellでvenvを作成・有効化</h3>

※有効化は毎回開発時にやる（powershellの場合）

```
PowerShell Set-ExecutionPolicy RemoteSigned CurrentUser  #実行ポリシーを変更
py -m venv venv  #venvフォルダの作成（※プロジェクト直下にできます）
venv\Scripts\Activate.ps1   #最後はps「イチ」
```

<h3>最新のpipを入れる</h3>

```
python -m pip install --upgrade pip
```
<h3>requirements.txt を参照して必要な外部ライブラリー（・パッケージ）を一括インストール</h3>

```
pip install -r requirements.txt
```

<h3>.envをappsフォルダと同じ階層に作成（環境変数（の一部）の設定）</h3>

※.gitignoreでpush時除外されます（同様にSECRET_KEY、WTF_CSRF_SECRET_KEYを設定）

```.env
FLASK_APP=apps.app:create_app
FLASK_ENV=development
```

正しいか分からないですが、よくこれを利用してます
<a href="https://qiita.com/Scstechr/items/c3b2eb291f7c5b81902a">Pythonのランダム文字列生成（※インタラクティブシェルを通して利用）</a>

<h3>ルーティングの確認</h3>

```
flask routes
```

<h3>DBの作成</h3>

```
flask db init
flask db migrate
flask db upgrade
```
※ロールバック時

```
flask db downgrade
```

<h3>開発用サーバー起動</h3>

```
flask run --debug
```
# object_detection_app
