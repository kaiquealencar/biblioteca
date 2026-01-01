from csv import reader
import os, pdb

from flask import Blueprint, request, redirect, render_template, flash, url_for, jsonify, session
from sqlalchemy import or_
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
        livro_id = request.form.get('livro_id')

        if not LoanService.consultar_disponibilidade_livro(livro_id):
            flash("Livro não disponível para empréstimo", "error")
            return redirect(url_for("emprestimos.cadastrar_emprestimos"))
                   
        valid_fields = ["leitor_id", "livro_id", "data_emprestimo", "data_devolucao", "status", "observacao"]              

        emprestimo_data = {k: v for k, v in data.items() if k in valid_fields}
        emprestimo = LoanService.create(**emprestimo_data)  
        
        flash("Empréstimo salvo com sucesso", "success")
        return redirect(url_for("emprestimos.cadastrar_emprestimos"))

    return render_template("emprestimo/emprestimo.html", leitores=lista_leitores, livros=lista_livros)


@loan_bp.route("/buscar-leitor", methods=["POST"])
def buscar_leitor():            
    termo = request.form.get("busca-leitor", "").strip()

    if not termo:
        return jsonify({"error": "Termo de busca vazio"}), 400

    leitor = Reader.query.filter(or_(Reader.nome.ilike(f"%{termo}%"), Reader.cpf.contains(termo))).first()

    if leitor:
        return jsonify({
            "id": leitor.id,
            "matricula": f"{leitor.numero_matricula:05d}",
            "nome": leitor.nome,
            "cpf": leitor.cpf
        }), 200
    
    return jsonify({"error": "Leitor não encontrado"}), 404

@loan_bp.route("/buscar-livro", methods=["POST"])
def buscar_livro():           
    termo = request.form.get("busca-livro", "").strip()

    if not termo:
        return jsonify({"error": "Termo de busca vazio"}), 400

    livro = Book.query.filter(or_(Book.titulo.ilike(f"%{termo}%"), Book.isbn.contains(termo))).first()

    if livro:
        return jsonify({
            "id": livro.id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "isbn": livro.isbn
        }), 200
    
    return jsonify({"error": "Livro não encontrado"}), 404

@loan_bp.route("/consultar-emprestimos", methods=["GET"])
def consultar_emprestimos():
    lista_emprestimos = []

    leitor = request.args.get("filtro_leitor", "").strip()
    livro = request.args.get("filtro_livro", "").strip()
    status = request.args.get("filtro_status", "").strip()

    resultados = LoanService.search(leitor, livro, status)

    lista_emprestimos = resultados if resultados is not None else []    
    return render_template("emprestimo/consultar_emprestimos.html", emprestimos=lista_emprestimos)

@loan_bp.route("/emprestimos", methods=["GET"])
def listar_emprestimos():
    return render_template("emprestimo/lista_emprestimos.html")    

@loan_bp.route("/devolver-emprestimo/<int:emprestimo_id>", methods=["POST"])
def devolver_emprestimo(emprestimo_id):
    emprestimo = LoanService.get_by_id(emprestimo_id)
    
    if not emprestimo:
        flash("Empréstimo não encontrado", "danger")
        return redirect(url_for("emprestimos.consultar_emprestimos"))

    LoanService.devolver_emprestimo(emprestimo_id)

    flash("Empréstimo devolvido com sucesso", "success")
    return redirect(url_for("emprestimos.consultar_emprestimos", emprestimo_id=emprestimo_id))    