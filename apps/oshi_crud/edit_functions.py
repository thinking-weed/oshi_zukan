from flask import current_app
from werkzeug.utils import secure_filename
import os

def save_image(image_file):
    # アップロードされたファイル名を安全に取得
    filename = secure_filename(image_file.filename)
    
    # 画像の保存先ディレクトリを取得
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    # 保存先の完全パスを作成
    file_path = os.path.join(upload_folder, filename)
    
    # 画像ファイルを保存
    image_file.save(file_path)
    
    # ファイル名を返す（後でデータベースに保存するため）
    return filename