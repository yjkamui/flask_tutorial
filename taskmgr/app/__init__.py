import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def create_app():
	app=Flask(__name__,instance_relative_config=True)
	app.config.from_pyfile('config.py')
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route('/')
	def hello():
		return '<h1>Hello, World.'

	db.init_app(app)

	with app.app_context():
		from .models import User
		db.create_all()

	return app

