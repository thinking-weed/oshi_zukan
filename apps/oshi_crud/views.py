import os,uuid
#アップロードされたファイル名をそのまま利用するとセキリティ上の問題がある可能性があるため、
#ここではアップロードファイル名をuuid形式に変換
#安全なファイル名に変換するwerkzeug.utilsにsecure_filename()関数があるが、ファイル名が日本語の場合に
# 動作しないケースがあるらしく、ここでは利用しない
from pathlib import Path
from sqlalchemy import desc
from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    current_app,
    send_from_directory,
    redirect,
    url_for,
    flash,
    request
)
from flask_login import current_user,login_required
from apps.app import db
from apps.oshi_crud.models import Oshi
from apps.user_crud.models import User
from apps.oshi_crud.forms import OshiForm
from apps.oshi_crud.detect_functions import (
    make_color,
    make_line,
    draw_lines,
    draw_texts,
    exec_detect
)

#Blueprintでuser_crudアプリを生成する
#apps直下のstaticを全体に適用する場合、blueprint作成時に
# url_prefixを指定せずにstatic_folder="static"を記述しない
oshi_crud = Blueprint(
    "oshi_crud",
    __name__,
    template_folder="templates"
)

#----------------------------------------------------------------------------------------------

@oshi_crud.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = OshiForm()
    # フォームの値をバリデートする
    #.validate_on_submitはフォームからsubmitされた際に実行されるやつ
    if form.validate_on_submit():
        #formにポストの投稿日時を取得して表示形式を変換
        first_posted_at_data = request.form.get('real_posted_at')
        posted_at_data = datetime.strptime(first_posted_at_data, '%Y-%m-%dT%H:%M')
        formatted_date = posted_at_data.strftime('%Y年%m月%d日 %H:%M')

        #アップロードされた画像ファイルを取得
        file = form.image.data
        # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
        # 安全なファイル名に変換するwerkzeug.utilsにsecure_filename()関数があるが、
        # ファイル名が日本語の場合に動作しないケースがあるため、参考書では利用していない
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        #画像を"imagesフォルダ"に保存する
        image_path = Path(
            current_app.config["UPLOAD_FOLDER"] , image_uuid_file_name
        )
        file.save(image_path)

        #Oshiの情報を"DB"に保存する
        oshi_info = Oshi(
            user_id = current_user.id,
            oshi_name=form.oshi_name.data,
            posted_at=str(formatted_date),
            # .datetime.strftime('%m月%d日%H時%M分')
            comment=form.comment.data,
            image_path = image_uuid_file_name
        )
        #登録情報を追加してコミット（＝変更反映）する
        db.session.add(oshi_info)
        db.session.commit()

        #一覧画面へリダイレクトする
        return redirect(url_for("oshi_crud.index"))
    #OshiFormで設定した「設定」をform=formで渡す
    #まだpost送信されていない状態の場合、登録画面をレンダリング
    return render_template("oshi_crud/create.html", form=form)

#----------------------------------------------------------------------------------------------

# 画像ファイルを提供するエンドポイント
@oshi_crud.route("/images/<path:filename>")
@login_required
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

#----------------------------------------------------------------------------------------------

# 画像一覧を表示するエンドポイント
@oshi_crud.route("/index")
@login_required
def index():
    form = OshiForm()
    #UserとOshiをJoin（テーブルを合体）して画像一覧を取得
    oshi_informations = (
        db.session.query(User,Oshi)
        .join(Oshi)
        .filter(User.id == Oshi.user_id)
        .order_by(desc("id"))#逆順に並べ替える
        .all()
    )
    return render_template("oshi_crud/index.html",oshi_informations=oshi_informations, form=form)

#----------------------------------------------------------------------------------------------

#コメント一覧を表示するエンドポイント
@oshi_crud.route("/comment_list")
@login_required
def comment_list():
    form = OshiForm()
    #UserとOshiをJoin（テーブルを合体）して画像一覧を取得
    oshi_informations = Oshi.query.all()
    return render_template("oshi_crud/comment_list.html",oshi_informations=oshi_informations, form=form)

#----------------------------------------------------------------------------------------------

#コメント編集をするためのエンドポイント（修正が必要）
@oshi_crud.route("/edit_info/<oshi_id>", methods=["GET", "POST", "PATCH"])
@login_required
def edit_info(oshi_id):
    # 指定されたidのレコードを取得
    oshi = Oshi.query.filter_by(id=oshi_id).first()
    
    # フォームを初期化する
    form = OshiForm(obj=oshi)

    # コロンで分割(maxsplit で最大分割数を指定)
    split_s = oshi.oshi_name.split('@', maxsplit=1)
    for_search = str(split_s[-1])

    # formからサブミットされた場合は推しの情報を更新し、画像一覧画面へリダイレクトする
    if form.validate_on_submit():
        oshi.oshi_name = form.oshi_name.data
        oshi.posted_at = form.posted_at.data
        oshi.comment = form.comment.data
        db.session.add(oshi)
        db.session.commit()
        return redirect(url_for("oshi_crud.index"))

    # GETの（=初回のまだ更新していない）場合はHTMLを返す
    return render_template("oshi_crud/edit_info.html", oshi=oshi, for_search=for_search, form=form)

#----------------------------------------------------------------------------------------------

#削除はPOSTしか利用しないので、methodsにはPOSTだけを指定
@oshi_crud.route("/<oshi_id>/delete", methods=["POST"])
@login_required
def delete(oshi_id):
    #指定されたidのレコードを取得
    oshi = Oshi.query.filter_by(id=oshi_id).first()
    db.session.delete(oshi)
    db.session.commit()
    return redirect(url_for("oshi_crud.index"))
#削除後、idは自動的に修正される

#-----------------------------------------------------------------------------------------------

