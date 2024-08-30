import logging,os
# os : オペーレーティングシステムが提供する様々な機能を利用できるモジュール
#os.environ.～で環境変数設定が一番頻出そう
from flask_debugtoolbar import DebugToolbarExtension
from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    current_app,
    g,
    flash
)
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

#ログレベルを設定
app.logger.setLevel(logging.DEBUG)

#リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

#DebugToolbarExtensionにアプリケーションをセット
toolbar = DebugToolbarExtension(app)

#Mailクラスのコンフィグを追加する
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
app.config["TESTING"] = False

email = app.config["MAIL_USERNAME"]


# flask-mail拡張を登録する
mail = Mail(app)

#メールを送信する関数
#テキストメールとHTMLメールの両方を作成して送信する。HTMLメールが受信できない場合、テキストメールが送信される

#to :メールの受信者のアドレス
#subject :メールの件名を指定
#template:メールのテンプレートファイル名を指定（拡張子は含まない）。
# '**kwargs'はテンプレートに渡す追加のキーワード引数を指定。
def send_email(to, subject, template, **kwargs):
    """通知メールを送信する関数"""
    app.logger.debug("Sending email...")
    try:
        msg = Message(subject, recipients=[to])
        msg.body = render_template(template + ".txt", **kwargs)
        msg.html = render_template(template + ".html", **kwargs)
        mail.send(msg)
        app.logger.debug("Email sent successfully.")
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        flash("メール送信に失敗しました。")

@app.route("/")
def index():
    return "Hello, Flask"

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/sent-mail", methods=["GET","POST"])
def contact_sent_mail():
    if request.method == "POST": #このチェックはどの時点で？？
        # POST送信されたフォームの値を取得する
        oshi_name = request.form["oshi_name"]

        # 画像ファイルは何か別の属性が必要か？？※下のコメントを取るとエラーになる
        # post_image = request.form["post_image"]
        posted_at = request.form["posted_at"]
        comment = request.form["comment"]

        # 入力チェック
        is_valid = True

        if not oshi_name:
            flash("Xアカウント名を入力してください")
            is_valid = False

        if not posted_at:
            flash("投稿日を入力してください")
            is_valid = False

        if not comment:
            flash("コメントを入力してください")
            is_valid = False

        #バリデーションに引っかかった場合
        if not is_valid:
            return redirect(url_for("contact"))

#-------------------------------------------------------------------------------------------
        #メールを送る
        send_email(
            email,
            "登録しました",
            "notification_mail",
            oshi_name = oshi_name,
            posted_at = posted_at,
            comment = comment
        )

        #flashメッセージはセッションが必要
        flash("登録内容を設定のメールに送信しました。")

        #リダイレクト (redirect): ユーザーを別のURLに移動させる。⇒エンドポイントが変わる
        # ユーザーが異なるURLに再度リクエストを送信することを意味する
        return redirect(url_for("contact_sent_mail"))
    
    #レンダリング (render_template): 現在のURLのままで指定されたテンプレートを表示⇒エンドポイントは変わらない？？
    #「/contact」になっている？？
    # れはサーバーからHTMLが直接返されることを意味する
    return render_template("contact_sent_mail.html")

# ----------------- 現在のルート情報をurl_for関数で出力 --------------------
#------------------ flask runでサーバーを起動するとurl_forで指定したエンドポイントの値が確認できる--------------------
#------------------エンドポイントがターミナル途中に出力される----------------------

with app.test_request_context():
    # /
    print(url_for("index"))
    # /hello/world
    #以下から分かるように、url_forの第一引数はあくまで「エンドポイント」
    print(url_for("hello-endpoint", name="world"))
    # /name/ichiro?page=1
    print(url_for("show_name", name="ichiro", page=1))
