from sqlalchemy.sql import func
from app.extensions import db
from datetime import datetime


class Reader(db.Model):

    __tablename__ = "reader"

    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf  = db.Column(db.String(14), unique=True, nullable=False, index=True)
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    logradouro = db.Column(db.String(255), nullable=False)
    bairro = db.Column(db.String(180), nullable=False)
    cidade = db.Column(db.String(180), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    numero_endereco = db.Column(db.String(15), nullable=False)
    numero_matricula = db.Column(db.Integer, unique=True, nullable=False, index=True)
    limite_emprestimo = db.Column(db.Integer, nullable=True, default=3)
    emprestimos_ativos = db.Column(db.Integer, default=0)
    observacao = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ultimo_emprestimo = db.Column(db.DateTime, nullable=True)
    responsavel = db.Column(db.String(255), nullable=True)
    telefone_responsavel = db.Column(db.String(15), nullable=True)
    obs_interna = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="ativo")
    foto = db.Column(db.String(255), nullable=True)
    

    

    def __repr__(self):
        return f"<Reader {self.nome} - {self.numero_matricula}>"        