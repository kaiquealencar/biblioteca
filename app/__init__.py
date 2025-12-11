from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .extensions import db
from .models import book

db = SQLAlchemy()

def create_app(config_object= "config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from .livros.routes import livros_bp
    app.register_blueprint(livros_bp)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    db.init_app(app)

    return app