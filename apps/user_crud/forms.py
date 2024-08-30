#ここではフォームの値やバリデータの属性の設定をクラスで指定
#-->HTMLの簡潔化、バリデートチェック漏れを防ぎやすくなる
from flask_wtf import FlaskForm
#以下importしている～Fieldはブラウザのフォームを構成するパーツとなる
from wtforms import PasswordField, StringField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Email, length

#ユーザー新規作成とユーザー編集フォームクラス

#FlaskFormクラスを継承してUserFormを作成

class UserForm(FlaskForm):
    #ユーザーフォームのusername属性のラベルとバリデータを設定
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired(message="ユーザー名は必須です。"),
            length(max=30, message="30文字以内で入力してください。")
        ]
    )

    #ユーザーフォームemail属性のラベルとバリデータを設定する
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須です。"),
            Email(message="メールアドレスの形式で入力してください")
        ],
    )
    
    #ユーザーフォームpassword属性のラベルとバリデータを設定する
    password = PasswordField(
        "パスワード",
        validators=[DataRequired(message="パスワードは必須です。")]
    )
    #ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("新規登録")


