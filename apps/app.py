from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from datetime import datetime
import logging,pytz
# import config なぜか、このコメントアウトを取り、
# apps.config.Configをconfig.Configとするとエラーになる

#SQLAlchemyをインスタンス化
db = SQLAlchemy()

#CSRFProtectをインスタンス化する
csrf = CSRFProtect()

#LoginManagerをインスタンス化する
login_manager = LoginManager()

#login_view属性に未ログイン時にリダイレクトするエンドポイントを指定
login_manager.login_view = "auth.signup"

# login_message属性にログイン後に表示するメッセージを指定する
# 下の1行をコメントアウトすると、デフォルトの英語のメッセージが出力される
# login_manager.login_message = "無事にログインしました。"

def create_app():
    #__name__は現在のモジュールの名前に置き換わる特殊変数
    app = Flask(__name__)

    #アプリケーションが使用するデフォルト設定をセット
    app.config.from_object('apps.config.Config')
    
    #ログレベルを設定
    app.logger.setLevel(logging.DEBUG)

    #DebugToolbarExtensionにアプリをセット
    toolbar = DebugToolbarExtension(app)

    #SQLAlchemyとアプリを連携（初期化）
    db.init_app(app)

    #Migrateとアプリを連携
    Migrate(app, db)

    #CSRFProtectインスタンスをアプリと連携
    csrf.init_app(app)

    # login_manageをアプリケーションと連携する
    login_manager.init_app(app)

    tokyo_tz = pytz.timezone('Asia/Tokyo')
    tokyo_time = datetime.now(tokyo_tz)


#---------------------------各Blueprintを以下に定義-----------------------------------

#---------------------------開発用サーバー起動時（スタートメニュー）---------------------------
    from apps.start import views
    app.register_blueprint(views.start, url_prefix="/")

#-------------------ユーザー情報------------------------------------------------------
#------------------------------------------------------------------------------------

    #user_crudパッケージからviewsをimportする
    from apps.user_crud import views

    # register_blueprintを使いviews.pyのuser_crudアプリを登録
    app.register_blueprint(views.user_crud, url_prefix="/user_crud")

#------------------------------------------------------------------------------------

    from apps.auth import views

    app.register_blueprint(views.auth, url_prefix="/auth")

#---------------------------推し図鑑--------------------------------------------

    from apps.oshi_crud import views

    app.register_blueprint(views.oshi_crud)

    return app


