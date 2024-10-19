# object_detection_app（推し図鑑（自分の推しの画像収集図鑑）・画像検知アプリ）

git clone後以下のコマンドで動くはず・・・（Pythonのversionは3.9.6を使用しています）

<h3>powershellでvenvを作成・有効化</h3>

※有効化は毎回開発時にやる（powershellの場合）

```
PowerShell Set-ExecutionPolicy RemoteSigned CurrentUser  #実行ポリシーを変更
py -m venv venv  #venvフォルダの作成（※プロジェクト直下にできます）
.\venv\Scripts\Activate.ps1   #最後はps「イチ」
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
SECRET_KEY=
WTF_CSRF_SECRET_KEY=
```

正しいか分からないですが、よくこれを利用してます
<a href="https://qiita.com/Scstechr/items/c3b2eb291f7c5b81902a">Pythonのランダム文字列生成（※インタラクティブシェルを通して利用）</a>

<h3>ルーティングの確認</h3>

```
flask routes
```

<h3>Pytorchにデフォルトで用意されている学習済みモデルmodel.ptファイルを取得</h3>
ターミナルを開き

```powershell
～～\object_detection_app>python
```
でインタラクティブシェルを起動して以下のように入力してください

```powershell
～～\object_detection_app>python
Python 3.9.6 (tags/v3.9.6:db3ff76, Jun 28 2021, 15:26:21) [MSC v.1929 64 bit (AMD64)] on win32　　　👈メッセージが出てきます
Type "help", "copyright", "credits" or "license" for more information.　　　　　　　　　　　　　　　　　※最後exit()+Enterで終了
>>>import torch
>>>import torchvision
>>>model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
>>>torch.save(model, "model.pt")
```
object_detection_app直下にmodel.ptというファイルが作成されたら、exit()+Enterでインタラクティブシェルを終了し、<br>
model.ptを以下の場所に入れてください。

```
object_detection_app
   |
   |--apps
        |
      oshi_crudフォルダ  👈ココの直下に入れる
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

<h2>もしよければ参考に</h2>

https://qiita.com/thinking-weed/items/702bc7353edb644e567d
