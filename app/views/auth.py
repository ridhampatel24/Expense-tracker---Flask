from flask import session, make_response, redirect, render_template, url_for, flash
from app.forms import LoginForm, RegisterForm
from app.models import UserInfo
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from app import app
from app.extensions import db
import jwt
import bcrypt
import os


def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = str(login_form.password.data)
        isuser = UserInfo.query.filter_by(email=email).first()
        if isuser:
            try: 
                if bcrypt.checkpw(password.encode("utf-8"), bytes(isuser.password, "utf-8")):
                    session["profile_photo"] = isuser.profile_photo

                    token = jwt.encode(
                        {
                            "public_id": isuser.id,
                            "exp": datetime.utcnow() + timedelta(minutes=30),
                        },
                        app.config["SECRET_KEY"],
                    )
                    response = make_response(redirect(url_for("item_route.home")))
                    response.set_cookie("Authorization", token)

                    return response
                else:
                    flash("Incorrect password for given email...", "alert")
                    return redirect(url_for("auth_route.login"))
            except ValueError as e:
                flash("Incorrect password or email!", "alert")
                return redirect(url_for("auth_route.login"))
        else:
            flash("Incorrect email address...", "alert")
            return redirect(url_for("auth_route.login"))
    return render_template("login.html", form=login_form)


def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        name = register_form.name.data
        email = register_form.email.data
        password = str(register_form.password.data)
        image = register_form.profile_photo.data
        filename = secure_filename(image.filename) + str(datetime.now().timestamp())
        image.save(os.path.join(app.config["IMAGES_UPLOADS"], filename))
        profile_photo = url_for("static", filename=f"images/{filename}")
        new_user = UserInfo(
            name=name, email=email, profile_photo=profile_photo
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session["profile_photo"] = new_user.profile_photo

        token = jwt.encode(
            {
                "public_id": new_user.id,
                "exp": datetime.utcnow() + timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
        )
        response = make_response(redirect(url_for("item_route.home")))
        response.set_cookie("Authorization", token)

        return response

    return render_template("signup.html", form=register_form)


def logout():
    session["profile_photo"] = None
    response = make_response(redirect(url_for("auth_route.index")))
    response.delete_cookie("Authorization")
    flash("Logged out successfully...", "success")
    return response
