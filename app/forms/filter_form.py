""" Importing wtform moduls """
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class FilterForm(FlaskForm):
    """ FilterForm use to get filter property """
    filter_name = SelectField(choices=[], validate_choice=False)
    submit = SubmitField("Filter")
