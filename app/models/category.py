from app.extensions import db
from flask_sqlalchemy import *


class Category(db.Model):
    __tablename__ = "category"
    __searchable__ = ["name"]
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    owner_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    category_status = db.Column(db.Integer, nullable=False, default=1)
    item = db.relationship("Item", cascade="all,delete", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"
