from datetime import datetime

from apps.app import db

class Oshi(db.Model):
    #テーブル名を指定
    __tablename__ = "oshi_informations"
    #カラムを定義
    id = db.Column(db.Integer, primary_key=True)
    #usersテーブルのidカラムを外部キーとして設定
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    oshi_name = db.Column(db.String)
    posted_at = db.Column(db.String)
    comment = db.Column(db.String)
    image_path = db.Column(db.String,nullable=True)
    is_detected = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

#db.Modelを継承したOshiImageTagクラスを作る
class OshiImageTag(db.Model):
    #テーブル名を指定
    __tablename__ = "oshi_image_tags"
    id = db.Column(db.Integer, primary_key=True)
    #oshi_image_idはoshi_informationsテーブルのidカラムの外部キーとして設定
    oshi_image_id = db.Column(db.String, db.ForeignKey("oshi_informations.id"))
    tag_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)





