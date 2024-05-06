""" Importing wtform moduls """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddCategory(FlaskForm):
    """ AddCategory form use to add or edit category details """
    name = StringField("Category name", validators=[DataRequired()])
    submit = SubmitField("Add Category")
