from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from datetime import datetime

class Loan(db.Model):
    __tablename__ = "loans"
    
    id = db.Column(db.Integer, primary_key=True)
    leitor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    data_saida = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_prevista = db.Column(db.DateTime, nullable=False)
    data_retorno = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pendente')
    multa_aplicada = db.Column(db.Float, default=0.0)

    leitor = db.relationship('User', backref=db.backref('loans', lazy=True))
    livro = db.relationship('Book', backref=db.backref('loans', lazy=True)) 

    def __repr__(self):
        return f"<Loan {self.id}>"