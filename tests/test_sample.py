#fixtures（フィクスチャ）テスト関数の前後に処理を実行する機能
#例 DBを使ったテストをする場合、テスト関数実行前にDBのセットアップ処理を行い、
#   テスト関数実行後にクリーンナップ処理（データベースのクリア）を行う

import pytest

def test_func1():
    assert 1 == 1

def test_func2():
    assert 1 == 2

# @pytest.fixtureを追加する
# @pytest.fixture
# def app_data():
#     return 3

# フィクスチャの関数を引数で指定すると関数の実行結果が渡される
def test_func3(app_data):
    assert app_data == 3
