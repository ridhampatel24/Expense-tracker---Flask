""" Importing wtform moduls """
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    """ SearchForm contain one field to search for item, bank, category """
    q = StringField(
        "Search", validators=[DataRequired()], render_kw={"placeholder": "Search ..."}
    )

    def __init__(self, *args, **kwargs):
        if "formdata" not in kwargs:
            kwargs["formdata"] = request.args
        if "meta" not in kwargs:
            kwargs["meta"] = {"csrf": False}
        super(SearchForm, self).__init__(*args, **kwargs)
