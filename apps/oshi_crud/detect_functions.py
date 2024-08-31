import random
# OpenCV（画像や動画の処理ができる機能がまとめられたオープンソースライブラリ）
# opencv-python が対応
import cv2
from flask import (
    current_app,
)

#画像処理系関数

# 枠線の色をランダム
def make_color(labels):
    #random.randint(0, 255) を使って、RGBの各成分（赤、緑、青）のランダムな値（0から255の範囲）を生成
    # colors は labels の数だけランダムな色を生成してリストにする
    colors = [[random.randint(0,255) for _ in range(3)] for _ in labels]
    # colors リストからランダムに1つの色を選ぶ
    color = random.choice(colors)
    return color

#  枠線の太さを計算して返す関数を作成
# result_image は画像オブジェクト（例えば、OpenCVで読み込んだ画像）
def make_line(result_image):
    # result_image.shape[0:2] で画像の高さと幅を取得し、その中の大きい方を選ぶ
    # roundは四捨五入切り捨て
    line = round(0.002 * max(result_image.shape[0:2])) + 1
    return line

# 四角形の枠線を画像に追記
def draw_lines(c1, c2, result_image, line, color):
    cv2.rectangle(result_image, c1, c2, color, thickness=line)
    return cv2

#検知したテキストラベルを画像に追記
def draw_texts(result_image, line, c1, cv2, color, labels, label):
    #f""で変数を文字列に組み込む
    display_txt = f"{labels[label]}"
    font = max(line - 1, 1)
    t_size = cv2.getTextSize(
        display_txt, 0 ,fontScale=line / 3, thickness=font
    )[0]
    c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
    # テキストの背景を塗りつぶした四角形を描く
    cv2.rectangle(result_image, c1, c2, color, -1)
    cv2.putText(
        result_image,
        display_txt,
        (c1[0], c1[1] - 2),
        0,
        line / 3,
        [225, 255, 255],
        thickness=font,
        #lineType=cv2.LINE_AA でアンチエイリアス（滑らかに描画）
        lineType = cv2.LINE_AA
    )
    return cv2

def exec_detect(target_image_path):
    #ラベルの読み込み
    labels = current_app.config["LABELS"]