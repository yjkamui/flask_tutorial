import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Fine for local development; set NEWSAPP_SECRET_KEY before deploying anywhere real.
SECRET_KEY = os.environ.get('NEWSAPP_SECRET_KEY', 'dev-secret-key-change-me')
