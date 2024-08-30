from flask import Blueprint, render_template, redirect, url_for
from apps.app import db
from apps.user_crud.models import User
from apps.user_crud.forms import UserForm
from flask_login import login_required

#Blueprintでuser_crudアプリを生成する
user_crud = Blueprint(
    "user_crud",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@user_crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    # UserFormをインスタンス化する
    form = UserForm()
    # フォームの値をバリデートする
    #.validate_on_submitはフォームからsubmitされた際に実行されるやつ
    if form.validate_on_submit():
        #ユーザーを作成する
        #ここでapps/user_crud/forms.pyで設定したパーツを用いる
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        #ユーザーを追加してコミット（＝変更反映）する
        db.session.add(user)
        db.session.commit()
        #ユーザーの一覧画面へリダイレクトする
        return redirect(url_for("user_crud.users_index"))
    #UserFormで設定した「設定」をform=formで渡す
    #下のrender_templateで指定するHTMLの値がuser_crud/create.htmlとなっていることに注意
    return render_template("user_crud/create_user.html", form=form)

@user_crud.route("/users/index")
@login_required
def users_index():
    """ユーザーの一覧を取得する"""
    users = User.query.all() #db.session.query(User).all()と同じ
    return render_template("user_crud/users_index.html",users=users)

# ユーザー編集画面のエンドポイント
#デコレータのRule（第一引数）に変数を<>で組み込む
@user_crud.route("/users/<user_id>", methods=["GET","POST"])
@login_required
def edit_user(user_id):
    form = UserForm()

    #Userモデルを利用してユーザーを取得する
    #指定されたidのレコードを取得 ※複数引数（=条件）を渡した場合はAND条件となる
    user = User.query.filter_by(id=user_id).first()

    # formからサブミットされた場合はユーザーを更新し、ユーザーの一覧画面へリダイレクトする
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_crud.users_index"))
    
    #GETの（=初回のまだ更新していない）場合はHTMLを返す
    #user = User.query.filter_by(id=user_id).first()で取得したuserをuserという変数名で渡す
    #form = UserForm()をformという変数名で渡す
    return render_template("user_crud/user_edit.html", user=user, form=form)

#削除はPOSTしか利用しないので、methodsにはPOSTだけを指定
@user_crud.route("/users/<user_id>/delete",methods=["POST"])
@login_required
def delete_user(user_id):
    #指定されたidのレコードを取得
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("user_crud.users_index"))
#削除後、idは自動的に修正される
