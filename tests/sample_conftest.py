# 複数のテストファイルでフィクスチャを共有するには、このようなconftestファイル（config & test ？？）を作ることで
# testsフォルダ配下のすべてのテストでフィクスチャを使用できる。

import pytest

@pytest.fixture
def app_data():
    return 3