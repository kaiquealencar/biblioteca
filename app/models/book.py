from flask_sqlalchemy import SQLAlchemy
from app.extensions import db


class Book(db.Model):
    __tablename__ = "books"
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(17), nullable=False)
    ano_pub = db.Column(db.Integer, nullable=False)
    editora = db.Column(db.String(150), nullable=False)
    paginas = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(100), nullable=False)
    formato = db.Column(db.String(50), nullable=False)
    idioma = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    capa_livro = db.Column(db.String(255), nullable=False)
    disponivel = db.Column(db.Boolean, default=True, nullable=False)
    
    
    def __init__(self, titulo, autor, isbn, ano_pub, editora, paginas,
                 genero, formato, idioma, descricao, capa_livro, disponivel=True):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ano_pub = ano_pub
        self.editora = editora
        self.paginas = paginas
        self.genero = genero
        self.formato = formato
        self.idioma = idioma
        self.descricao = descricao
        self.capa_livro = capa_livro
        self.disponivel = disponivel


    def __repr__(self):
        return f"<Book {self.titulo} - {self.autor}>"