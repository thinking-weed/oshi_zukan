from apps.app import db
from apps.auth.forms import SignUpForm, LoginForm
from apps.user_crud.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@auth.route("/")
def auth_index():
    return render_template("auth/auth_index.html")

#--------------サインアップ-------------------------------

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    #SignUpFormをインスタンス化する
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )

        #メールアドレスを重複チェック
        # models.pyで定義した関数
        if user.is_duplicate_email():
            flash("指定のメールアドレスは登録済みです")
            return redirect(url_for("auth.signup"))
        
        #ユーザー情報を登録する
        db.session.add(user)
        db.session.commit()

        #ユーザー情報をセッションに格納する
        login_user(user)
        #GETパラメータにnextキーが存在し、値がない場合はユーザーの一覧ページへリダイレクト
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("oshi_crud.index")
        return redirect(next_)
    
    return render_template("auth/signup.html", form = form)

#--------------ログイン-------------------------------

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #メールアドレスからユーザーを取得する
        user = User.query.filter_by(email=form.email.data).first()

        # ユーザーが存在しパスワードが一致する場合はログインを許可する
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("oshi_crud.index"))
        
        # ログイン失敗メッセージを設定する
        flash("メールアドレスかパスワードが不正です。")
    return render_template("auth/login.html", form = form)

#------------ログアウト-----------------------------------

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))



