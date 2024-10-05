from flask import Blueprint, render_template, redirect, url_for
from apps.app import db
from apps.user_crud.models import User
from apps.user_crud.forms import UserForm
from apps.oshi_crud.models import Oshi
from apps.oshi_crud.forms import OshiForm

#Blueprintでstartアプリを生成する
start = Blueprint(
    "start",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@start.route("")
def menu():
    return render_template("start/start_menu.html")

