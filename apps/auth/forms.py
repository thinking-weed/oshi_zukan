#ここではあくまで認証機能で使う各パーツの「設定」をしている

from flask_wtf import FlaskForm
#以下importしている～Fieldはブラウザのフォームを構成するパーツとなる
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

#FlaskFormクラスを継承してUserFormを作成

class SignUpForm(FlaskForm):
    #ユーザーフォームのusername属性のラベルとバリデータを設定
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired("ユーザー名は必須です。"),
            Length(1, 30, "30文字以内で入力してください。")
            #1文字以上30字以内で入力、第三引数はバリデーションエラーメッセージ
        ]
    )

    #ユーザーフォームemail属性のラベルとバリデータを設定する
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            #メールアドレスはメールアドレスの形式だけに制限
            Email("メールアドレスの形式で入力してください。")
        ]
    )
    
    #ユーザーフォームpassword属性のラベルとバリデータを設定する
    password = PasswordField(
        "パスワード",
        validators=[DataRequired("パスワードは必須です。")]
    )
    #ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("新規登録")

class LoginForm(FlaskForm):
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレスの形式で入力してください。")
        ]
    )
    password = PasswordField(
        "パスワード",
        validators=[DataRequired("パスワードは必須です。")]
    )
    submit = SubmitField("ログイン")