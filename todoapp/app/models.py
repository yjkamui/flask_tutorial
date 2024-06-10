from . import db
from flask_login import UserMixin
from datetime import datetime
import pytz

class User(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(50),nullable=False)
	password=db.Column(db.String(128),nullable=False)

class Task(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	taskname=db.Column(db.String(100),nullable=False)
	created_at=db.Column(db.DateTime,default=datetime.now(pytz.timezone('Asia/Tokyo')))
	due_date=db.Column(db.DateTime)

