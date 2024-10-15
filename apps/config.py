"""FlaskのConfigを提供する"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import random, string, os

#ランダム文字列生成関数
def random_strings(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)

# Pythonのpathlibモジュールを使って、
# 現在のスクリプトが置かれているディレクトリの「2つ上の階層」のディレクトリパスを取得するコード
# object_detection_app/apps/config.pyが__file__にあたるので、全体としてはobject_detection_app
basedir = Path(__file__).parent.parent

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')

    # SQLiteのデータベースを出力するパスを指定
    #Path(__file__):現在のPythonファイルのパスを表す
    #__file__: 現在のモジュールが定義されているファイルのパスを表す
    #.parent はその親ディレクトリを指す
    #/ 'local.sqlite' はそのディレクトリ内の local.sqlite という名前のSQLiteデータベースファイルを指定
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}"

    #SQLAlchemyは、デフォルトで全てのオブジェクトの変更を追跡し、
    #その情報を使ってセッションのコミット時に変更をデータベースに反映させる。
    #これらの変更追跡を無効にし、パフォーマンスを向上させる
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #SQLAlchemyが実行するSQLクエリがコンソールに出力されるか否か
    SQLALCHEMY_ECHO = True

    #リダイレクトを中断しないようにする
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    #画像アップロード先にapps/imagesを指定する
    #UPLOAD_FOLDERはFlaskに用意された環境変数
    UPLOAD_FOLDER = str(Path(basedir, "apps", "images"))

    # 物体検知に利用するラベル
    LABELS = [
        "unlabeled","person","bicycle","car","motorcycle","airplane","bus","train","truck","boat","traffic light",
        "fire hydrant","street sign","stop sign","parking meter","bench","bird","cat","dog","horse","sheep",
        "cow","elephant","bear","zebra","giraffe","hat","backpack","umbrella","shoe","eye glasses","handbag",
        "tie","suitcase","frisbee","skis","snowboard","sports ball","kite","baseball bat","baseball glove",
        "skateboard","surfboard","tennis racket","bottle","plate","wine glass","cup","fork","knife","spoon",
        "bowl","banana","apple","sandwich","orange","broccoli","carrot","hot dog",
        "pizza","donut","cake","chair","couch","potted plant","bed","mirror","dining table","window",
        "desk","toilet","door","tv","laptop","mouse","remote","keyboard","cell phone","microwave",
        "oven","toaster","sink","refrigerator","blender","book","clock","vase","scissors","teddy bear",
        "hair drier","toothbrush"
        # "microphone"
    ]

class TestingConfig(DevelopmentConfig):
    #テストで「アプリで利用する画像アップロードディレクトリ」を利用しないように、
    #UPLOAD_FOLDERを追加
    #画像アップロード先にtests/oshi_crud/imagesを指定する
    UPLOAD_FOLDER = str(Path(basedir, "tests", "oshi_crud", "images"))

Config = DevelopmentConfig
TestingConfig = TestingConfig
