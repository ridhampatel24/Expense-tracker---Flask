from app.extensions import db
from flask_sqlalchemy import *


class Bank(db.Model):
    __tablename__ = "bank"
    __searchable__ = ["name", "balance"]
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float(2), nullable=False)
    owner_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    item = db.relationship("Item", cascade="all,delete", backref="bank", lazy=True)
    bank_status = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"<Bank {self.name}>"
