from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .extensions import db, migrate


def create_app(config_object= "config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    from .livros.routes import livros_bp
    app.register_blueprint(livros_bp)

    from .auth.routes import usuario_bp
    app.register_blueprint(usuario_bp)

    
    db.init_app(app)
    migrate.init_app(app, db)

    return app