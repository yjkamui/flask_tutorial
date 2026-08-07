from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    with app.app_context():
        from .routes import article_bp, feed_bp
        app.register_blueprint(article_bp)
        app.register_blueprint(feed_bp)

        db.create_all()

        from .seeds import seed_default_feeds
        seed_default_feeds()

    return app
