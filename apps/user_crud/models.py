from datetime import datetime

from apps.app import db, login_manager

#flask-login拡張のログイン機能を利用するのに定義する必要がある関数やプロパティを含むクラスをimportする
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

#Userクラスをdb.Modelに加えてUserMixinを継承する
class User(db.Model, UserMixin):
    #テーブル名を指定
    __tablename__ = "users"
    #カラムを定義
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    #DateTimeは日付と時刻のデータを格納するカラムを定義
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    #backrefを利用しrelation情報を設定
    oshi_images = db.relationship("Oshi",backref="user")


    #パスワードをセットするためのプロパティ
    # @propertyはPythonの組み込みデコレータで、クラスのメソッドをプロパティのように扱うために使用される
    
    @property
    def password(self):
        raise AttributeError("読み取り不可")
    
    #パスワードをセットするためのセッター関数でハッシュ化したパスワードをセットする
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    #パスワードをチェックする
    #入力されたパスワードがDBのハッシュ化されたパスワードと一致するかをチェック
    # 一致する場合はTrueを返し、一致しない場合はFalseを返す
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #メールアドレス重複チェックする
    # DBに同じメールアドレスを持つレコードがある場合はtrueを返し、レコードがない場合はfalseを返す
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None

#ログインしているユーザー情報を取得する関数を作成
@login_manager.user_loader
def load_user(user_id):
    # ユーザーのユニークIDを引数で渡し、DBから特定のユーザーを取得して返す必要がある
    return User.query.get(user_id)

