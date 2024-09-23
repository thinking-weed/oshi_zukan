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
@pytest.fixture
def fixture_app():
    # セットアップ処理（アプリを作成し、データベースを初期化）
    # テスト用のコンフィグを使うために引数にtestingを指定する
    app = create_app("testing")

    #データベースを利用するための宣言をする
    app.app_context().push()

    