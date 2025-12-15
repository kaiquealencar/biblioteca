import os

from flask import Blueprint, request, redirect, render_template, flash, url_for, jsonify
from werkzeug.utils import secure_filename

from .service import BookService
from app.models import Book

livros_bp = Blueprint("livros", __name__)


@livros_bp.route("/cadastro-livro", methods=["GET", "POST"])
def cadastrar_livro():

    if request.method == "POST":
        data = request.form.to_dict()
        capa_livro = request.files.get("capa_livro")

        if capa_livro:
            upload_path = "static/uploads/capas"
            os.makedirs(upload_path, exist_ok=True)
            
            filename = secure_filename(capa_livro.filename)
            capa_livro.save(f"static/uploads/capas/{filename}")
            data["capa_livro"] = filename

        data["disponivel"] = data.get("disponivel") == "True"
        
        valid_fields = [ 'titulo','autor','isbn','ano_pub','editora','paginas',
            'genero','formato','idioma','descricao','tag','disponivel','capa_livro']
        
        book_data = {k: v for k, v in data.items() if k in valid_fields}

        book = BookService.create(**book_data)

        flash("Livro salvo com sucesso", "success")
        return redirect(url_for("livros.cadastrar_livro"))
    
    return render_template("livro/livro.html")

