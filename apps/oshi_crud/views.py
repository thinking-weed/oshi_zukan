import os, uuid, random, cv2, torch, torchvision
import numpy as np
#アップロードされたファイル名をそのまま利用するとセキリティ上の問題がある可能性があるため、
#ここではアップロードファイル名をuuid形式に変換
#安全なファイル名に変換するwerkzeug.utilsにsecure_filename()関数があるが、ファイル名が日本語の場合に
# 動作しないケースがあるらしく、ここでは利用しない
from pathlib import Path
from PIL import Image
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
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
from apps.oshi_crud.models import Oshi, OshiImageTag
from apps.user_crud.models import User
from apps.oshi_crud.forms import OshiForm,DetectorForm
from apps.oshi_crud.edit_functions import save_image
from apps.oshi_crud.detect_functions import (
    make_color,
    make_line,
    draw_lines,
    draw_texts,
    exec_detect,
    save_detected_image_tags
)

#Blueprintでuser_crudアプリを生成する
#apps直下のstaticを全体に適用する場合、blueprint作成時に
# url_prefixを指定せずにstatic_folder="static"を記述しない
oshi_crud = Blueprint(
    "oshi_crud",
    __name__,
    template_folder="templates",
    static_folder="static"
)

#----------------------------------------------------------------------------------------------

@oshi_crud.route("/create", methods=["GET", "POST"])
@login_required
def create():
    oshi_form = OshiForm()
    # フォームの値をバリデートする
    #.validate_on_submitはフォームからsubmitされた際に実行されるやつ
    if oshi_form.validate_on_submit():
        #formにポストの投稿日時を取得して表示形式を変換
        first_posted_at_data = request.form.get('real_posted_at')
        posted_at_data = datetime.strptime(first_posted_at_data, '%Y-%m-%dT%H:%M')
        # formatted_date = posted_at_data.strftime('%Y年%m月%d日 %H:%M')

        #アップロードされた画像ファイルを取得
        file = oshi_form.image.data
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
            oshi_name=oshi_form.oshi_name.data,
            posted_at=posted_at_data, #str(formatted_date),
            # .datetime.strftime('%m月%d日%H時%M分')
            comment=oshi_form.comment.data,
            image_path = image_uuid_file_name
        )
        #登録情報を追加してコミット（＝変更反映）する
        db.session.add(oshi_info)
        db.session.commit()

        #一覧画面へリダイレクトする
        return redirect(url_for("oshi_crud.index"))
    #OshiFormで設定した「設定」をform=formで渡す
    #まだpost送信されていない状態の場合、登録画面をレンダリング
    return render_template("oshi_crud/create.html", oshi_form=oshi_form)

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
    #UserとOshiをJoin（テーブルを合体）して画像一覧を取得
    oshi_informations = (
        db.session.query(User, Oshi)
        .join(Oshi)
        .filter(User.id == Oshi.user_id)
        .order_by(desc("id"))#逆順に並べ替える
        .all()
    )

    #画像に紐付くタグ一覧を取得し、画像IDをキーにした辞書にセット
    oshi_image_tag_dict = {}
    for oshi_info in oshi_informations:
        #画像に紐付くタグ一覧を取得する
        oshi_image_tags = (
            OshiImageTag.query.filter(OshiImageTag.oshi_image_id == oshi_info.Oshi.id)
            .all()
        )
        oshi_image_tag_dict[oshi_info.Oshi.id] = oshi_image_tags

    #物体検知フォームをインスタンス化
    detector_form = DetectorForm()
    #同様にフォームをインスタンス化
    oshi_form = OshiForm()
    return render_template(
        "oshi_crud/index.html",
        oshi_informations=oshi_informations,
        #タグ一覧をテンプレートに渡す
        oshi_image_tag_dict = oshi_image_tag_dict,
        #物体検知フォームをテンプレートに渡す
        detector_form = detector_form,
        oshi_form=oshi_form
    )

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
@oshi_crud.route("/edit_info/<oshi_id>", methods=["GET", "POST"])
@login_required
def edit_info(oshi_id):
    oshi = Oshi.query.filter_by(id=oshi_id).first_or_404()
    oshi_form = OshiForm(obj=oshi)

    split_s = oshi.oshi_name.split('@', maxsplit=1)
    for_search = str(split_s[-1])

    if oshi_form.validate_on_submit():
        oshi.oshi_name = oshi_form.oshi_name.data
        oshi.comment = oshi_form.comment.data

        # 新しい画像がアップロードされた場合のみ処理する
        if oshi_form.image.data:
            image_file = oshi_form.image.data
            image_filename = save_image(image_file)  # 画像保存関数
            oshi.image_path = image_filename  # 画像パスを更新

        db.session.commit()
        flash("情報が更新されました。", "success")
        return redirect(url_for("oshi_crud.index"))

    if oshi_form.errors:
        for field, errors in oshi_form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "danger")

    return render_template("oshi_crud/edit_info.html", oshi=oshi, for_search=for_search, oshi_form=oshi_form)



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

#--------------------------物体検知エンドポイント------------------------------------------------

@oshi_crud.route("/detect/<string:oshi_image_id>", methods=["POST"])
@login_required
def detect(oshi_image_id):
    oshi_image = (
        Oshi.query.filter(Oshi.id == oshi_image_id).first()
    )
    if oshi_image is None:
        flash("物体検知対象の画像が存在しません。")
        return redirect(url_for("oshi_crud.index"))
    
    #物体検知対象の画像パスを取得する
    target_image_path = Path(
        current_app.config["UPLOAD_FOLDER"], oshi_image.image_path
    )

    #物体検知を実行してタグと変換後の画像パスを取得する
    tags, detected_image_file_name = exec_detect(target_image_path)

    try:
        #データベースにタグと変換後の画像パス情報を保存する
        save_detected_image_tags(oshi_image, tags, detected_image_file_name)
    except SQLAlchemyError as e:
        flash("物体検知処理でエラーが発生しました。")
        #ロールバックする
        db.session.rollback()
        #エラーログ出力
        current_app.logger.error(e)
        return redirect(url_for("oshi_crud.index"))
    
    return redirect(url_for("oshi_crud.index"))

#-----------------------------物体検索エンドポイント-------------------------------------

@oshi_crud.route("/images/search", methods=["GET"])
@login_required
def search():
    #検索元となる画像一覧を取得する
    oshi_informations = db.session.query(User, Oshi).join(
        Oshi, User.id == Oshi.user_id
    ).order_by(desc("id"))#逆順に並べ替える

    #GETパラメータから検索ワードを取得する
    search_text = request.args.get("search")
    oshi_image_tag_dict = {}
    filtered_oshi_informations = []

    #oshi_informationsをループして、oshi_informationsに紐づくタグ情報を検索する
    for oshi_info in oshi_informations:
        #検索ワードが空の場合はすべてのタグを取得する
        if not search_text:
            #タグ一覧を取得する
            oshi_image_tags = (
                OshiImageTag.query
                .filter(OshiImageTag.oshi_image_id == oshi_info.Oshi.id)
                .all()
            )
        else:
            #検索ワードで絞り込んだタグを取得する（検索フォームに値を入力した場合）
            oshi_image_tags = (
                OshiImageTag.query
                .filter(OshiImageTag.oshi_image_id == oshi_info.Oshi.id)
                .filter(OshiImageTag.tag_name.like("%" + search_text + "%"))
                .all()
            )

            #タグが見つからなかったら（まだ検知してタグを生成していなかったら）画像を返さない
            if not oshi_image_tags:
                continue

            #タグがある（生成されている）場合はタグ情報を取得し直す
            oshi_image_tags = (
                OshiImageTag.query
                .filter(OshiImageTag.oshi_image_id == oshi_info.Oshi.id)
                .all()
            )
        
        #oshi_image_id をキーとする辞書にタグ情報をセットする
        oshi_image_tag_dict[oshi_info.Oshi.id] = oshi_image_tags

        #絞り込み結果のoshi_info情報を配列セットする
        filtered_oshi_informations.append(oshi_info)
    
    detector_form = DetectorForm()
    oshi_form = OshiForm()

    return render_template(
        "oshi_crud/index.html",
        # 検索で絞り込んだoshi_informations配列を渡す
        oshi_informations = filtered_oshi_informations,
        # 画像に紐付くタグ一覧の辞書を渡す
        oshi_image_tag_dict = oshi_image_tag_dict,
        detector_form = detector_form,
        oshi_form=oshi_form
    )

# 404エラーハンドリングデコレータ
@oshi_crud.errorhandler(404)
def page_not_found(e):
    return render_template("oshi_crud/404.html"), 404

# 500エラーハンドリングデコレータ
@oshi_crud.errorhandler(500)
def internal_server_error(e):
    return render_template("oshi_crud/500.html"), 500
