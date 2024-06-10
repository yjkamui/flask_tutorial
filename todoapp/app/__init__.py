from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager

db= SQLAlchemy()
login_manager=LoginManager()
login_manager.ligin_view='auth.login'

def create_app():
	app=Flask(__name__,instance_relative_config=True)
	app.config.from_pyfile('config.py')

	db.init_app(app)
	login_manager.init_app(app)

	with app.app_context():
		from .routes import auth_bp,index_bp,task_bp
		app.register_blueprint(auth_bp)
		app.register_blueprint(index_bp)
		app.register_blueprint(task_bp)

		db.create_all()
	return app

@login_manager.user_loader
def load_user(user_id):
	from .models import User
	return User.query.get(int(user_id))