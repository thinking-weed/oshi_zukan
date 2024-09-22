from flask import Flask,render_template

#登録したエンドポイント名の関数を作成し、404や500が発生した際に指定したHTMLを返す
def page_not_found(e):
    """404 Not Found"""
    return render_template("404.html"), 404

def internal_server_error(e):
    """500 Internal Server Error"""
    return render_template("500.html"), 500