from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length
from flask_wtf.file import FileAllowed, FileField, FileRequired
#ここではあくまでフォームで使う各パーツの「設定」をしている
#以下importしている～Fieldはブラウザのフォームを構成するパーツとなる

class OshiForm(FlaskForm):
    oshi_name = StringField(
        "推しの名前またはXアカウント名",
        validators=[
            DataRequired(message="入力必須です。")
        ]
    )
    posted_at = StringField(
        "投稿日時または写真日時"
    )
    comment = StringField(
        "推しへのコメント",
        validators=[
            DataRequired(message="コメントを入力してください。"),
            length(max=140, message="140文字以内で入力してください。")
        ]
    )
    #ファイルフィールドに必要なバリデーションを設定する
    image = FileField(
        validators=[
            FileRequired("画像ファイルを指定してください。"),
            #許可する拡張子を指定
            FileAllowed(["png", "jpg", "jpeg"],"サポートされていない画像形式です")
        ]
    )
    #submitの文言を設定する
    # SubmitFieldは<input type=file>フィールドを生成
    submit = SubmitField("追加")

class DetectorForm(FlaskForm):
    submit = SubmitField("検知")
