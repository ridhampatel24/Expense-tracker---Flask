from app.extensions import db
from flask_sqlalchemy import *
from datetime import datetime, timedelta
import bcrypt

class UserInfo(db.Model):
    __tablename__ = "userprofile"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_photo = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    amount = db.Column(db.Float(2), nullable=False, default=0.00)
    item = db.relationship("Item", cascade="all,delete", backref="userprofile", lazy=True)
    category = db.relationship(
        "Category", cascade="all,delete", backref="userprofile", lazy=True
    )
    bank = db.relationship("Bank", cascade="all,delete", backref="userprofile", lazy=True)
    deleted_bank = db.Column(db.Integer, nullable=False, default=0)
    deleted_category = db.Column(db.Integer, nullable=False, default=0)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password = pwhash.decode('utf8') 

    def __repr__(self):
        return f"<Userprofile {self.name}>"
