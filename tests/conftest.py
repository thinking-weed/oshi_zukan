# 複数のテストファイルでフィクスチャを共有するには、
# このようなconftestファイル（config & test ？？）を作ることで
# testsフォルダ配下のすべてのテストでフィクスチャを使用できる。
import os, shutil, pytest

#shutilはファイルやファイルの集まりに対する高水準の操作方法を多数提供するもの
#特にファイルのコピーや削除のための関数が用意されている。

from apps.app import create_app, db

from apps.user_crud.models import User
from apps.oshi_crud.models import Oshi, OshiImageTag

#フィクスチャ関数を作成する
#一連の処理は、テスト関数ごとに実行される
@pytest.fixture
def fixture_app():
    # セットアップ処理（アプリを作成し、データベースを初期化）
    # テスト用のコンフィグを使うために引数にtestingを指定する
    app = create_app("testing")

    #データベースを利用するための宣言をする
    app.app_context().push()

    #テスト用データベースのテーブルを作成する
    with app.app_context():
        db.create_all()

    #テスト用の画像アップロードディレクトリを作成する
    os.mkdir(app.config["UPLOAD_FOLDER"])

    #テストを実行する
    #フィクスチャ関数にyieldが含まれている場合は、ここでテストが実行される
    #テストが終了すると、yield以降の行のフィクスチャ関数の処理が実行される
    yield app

    #クリーンナップ処理（テスト実行後に作成されたデータベースをクリア）
    User.query.delete()

    #oshi_informationsテーブルのレコードを削除する
    Oshi.query.delete()

    #oshi_image_tagsテーブルのレコードを削除する
    OshiImageTag.query.delete()

    #テスト用の画像アップロードディレクトリを削除する
    shutil.rmtree(app.config["UPLOAD_FOLDER"])

    db.session.commit()

#Flaskのテストクライアントを返すフィクスチャ関数を作成
@pytest.fixture
def client(fixture_app):
    #Flaskのテスト用クライアントを返す
    return fixture_app.test_client()