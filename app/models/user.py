from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError("A senha não pode ser lida diretamente")
    
    @password.setter
    def password(self, senha):
        self.password_hash = generate_password_hash(senha)


    def check_password(self, senha):
        return check_password_hash(self.password_hash, senha)
