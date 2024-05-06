from flask import Blueprint, render_template
from app.utils.authenticate import have_token, token_required
from app.views import auth

auth_route = Blueprint("auth_route", __name__)


@auth_route.route("/")
@auth_route.route("/index")
@have_token
def index():
    return render_template("index.html")


@auth_route.route("/login", methods=["GET", "POST"])
@have_token
def login():
    return auth.login()


@auth_route.route("/signup", methods=["GET", "POST"])
@have_token
def signup():
    return auth.register()


@auth_route.route("/logout")
@token_required
def logout(user):
    return auth.logout()
