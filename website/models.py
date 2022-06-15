from email.policy import default
from . import db
from flask_login import UserMixin
from sqlalchemy import func, null

class Item(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable = False)
   notes = db.Column(db.String(200), nullable=False, default="")
   createdBy = db.Column(db.String(30), nullable = False)
   belongsTo = db.Column(db.Integer, db.ForeignKey('user.id'))
   date = db.Column(db.DateTime(timezone=True), default=func.now())
   fileName = db.Column(db.String(50), default="")

class Admin(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   firstName = db.Column(db.String(20), nullable = False)
   lastName = db.Column(db.String(20), nullable = False)
   email = db.Column(db.String(150), nullable = False)
   password = db.Column(db.String(150), nullable = False)

class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(40), nullable = False)
   items = db.relationship('Item')

class itemPool(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable = False)