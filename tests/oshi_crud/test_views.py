#conftest.pyのfixtureのclientを渡す
def test_index(client):
    #clientを使ってアプリケーションルートである/にGETでアクセス
    rv = client.get("/")
    assert "ログイン" in rv.data.decode()
    assert "新規登録" in rv.data.decode()
    #結果のrv.dataにはアクセスした結果の