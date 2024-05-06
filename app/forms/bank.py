""" Importing wtform moduls """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired


class AddBank(FlaskForm):
    """ AddBank form use to add or edit bank details """
    name = StringField("Bank name", validators=[DataRequired()])
    balance = DecimalField("Balance", places=2)
    submit = SubmitField("Add Bank")
