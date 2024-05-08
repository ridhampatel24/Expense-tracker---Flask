from app.extensions import db
from flask_sqlalchemy import *
from datetime import datetime

# from app.models.searchablemixin import SearchableMixin

# class Item(SearchableMixin, db.Model):


class Item(db.Model):
    __tablename__ = "item"
    __searchable__ = ["name", "price", "payment_mode", "transaction_date"]
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float(2), nullable=False)
    payment_mode = db.Column(db.String(20), nullable=False, default="cash")
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    bank_id = db.Column(
        db.Integer,
        db.ForeignKey("bank.id", ondelete="CASCADE"),
        nullable=True,
        default=None,
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("userprofile.id", ondelete="CASCADE"), nullable=False
    )
    transaction_date = db.Column(
        db.Date, nullable=False, default=datetime.today().strftime("%Y-%m-%d")
    )

    def __repr__(self):
        return f"<Item {self.name}>"
