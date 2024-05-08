from flask import redirect, url_for, request, flash
from functools import wraps
import jwt
import bcrypt
from app import app
from app.models.user import UserInfo


def have_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if request.cookies.get("Authorization"):
            token = request.cookies.get("Authorization")
        if not token:
            return f(*args, **kwargs)
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            flash("You can't login twice !")
            return redirect(url_for("item_route.home"))
        except:
            return f(*args, **kwargs)
        return f(*args, **kwargs)

    return decorated


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if request.cookies.get("Authorization"):
            token = request.cookies.get("Authorization")
        if not token:
            flash(
                "Unauthorize user, please login first or if not have account then signup...",
                "danger",
            )
            return redirect(url_for("auth_route.login"))

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = UserInfo.query.filter_by(id=data["public_id"]).first()
        except:
            flash("Unauthorize user, Your token is not authorize", "danger")
            return redirect(url_for("auth_route.login"))
        return f(current_user, *args, **kwargs)

    return decorated
