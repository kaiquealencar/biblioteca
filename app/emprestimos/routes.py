from csv import reader
import os 

from flask import Blueprint, request, redirect, render_template, flash, url_for, jsonify, session
from werkzeug.utils import secure_filename

from app import emprestimos
from app.models import Reader, Book
from .service import LoanService

from datetime import datetime

loan_bp = Blueprint("emprestimos", __name__)

@loan_bp.route("/cadastro-emprestimo", methods=["POST", "GET"])
def cadastrar_emprestimos():
    lista_leitores = Reader.query.all()
    lista_livros = Book.query.all() 

    if request.method == "POST":
        data = request.form.to_dict()
        

        valid_fields = ["leitor_id", "livro_id", "data_emprestimo", "data_devolucao", "status", "observacao"]
        emprestimo_data = {k: v for k, v in data.items() if k in valid_fields}
        emprestimo = LoanService.create(**emprestimo_data)  
        
        flash("Empréstimo salvo com sucesso", "success")
        return redirect(url_for("emprestimos.cadastrar_emprestimos"))

    return render_template("emprestimo/emprestimo.html", leitores=lista_leitores, livros=lista_livros)



@loan_bp.route("/emprestimos", methods=["GET"])
def listar_emprestimos():
    # Lógica para listar empréstimos
    return render_template("emprestimo/lista_emprestimos.html")     