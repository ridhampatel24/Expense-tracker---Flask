""" Importing wtform moduls """
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    """ RegisterForm use to get user details """
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    profile_photo = FileField(
        "Profile Photo",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png", "gif"], "Images only!"),
        ],
    )
    submit = SubmitField("Register")
