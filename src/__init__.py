import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from . import scraper


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key',
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)

    migrate.init_app(app, db)

    app.register_blueprint(scraper.bp)

    return app
