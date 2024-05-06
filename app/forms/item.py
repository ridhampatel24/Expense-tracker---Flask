""" Importing wtform moduls """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired


class AddItem(FlaskForm):
    """ AddItem form use to add or edit item details """
    name = StringField("Item name", validators=[DataRequired()])
    price = DecimalField("Amount", validators=[DataRequired()])
    category_name = SelectField("Category", choices=[], validate_choice=False)
    payment_mode = SelectField(
        "Payment type",
        choices=[("cash", "Cash"), ("upi", "UPI")],
        validate_choice=False,
    )
    bank_name = SelectField(
        "Bank name", choices=[("no_bank", "Through Cash")], validate_choice=False
    )
    submit = SubmitField("Add Item")
