from csv import reader
import os, re

from flask import Blueprint, request, redirect, render_template, flash, url_for, jsonify, session
from werkzeug.utils import secure_filename

from app import leitores

from .service import ReaderService
from app.service.arquivos_imagem import ServiceImage
from datetime import datetime

reader_bp = Blueprint("leitores", __name__)

@reader_bp.route("/cadastro-leitor", methods=["POST", "GET"])
def cadastrar_leitores():
    if request.method == "POST":
        data = request.form.to_dict()
        foto = request.files.get("foto")
        cpf_limpo = re.sub(r"\D", "", request.form.get("cpf", ""))
        data["cpf"] = cpf_limpo
        
        if data.get("data_nascimento"):
            data["data_nascimento"] = datetime.strptime(
                data["data_nascimento"], "%Y-%m-%d").date()
            
        
        if foto:
            data["foto"] = ServiceImage.salvar_image(foto, "leitores")

        if ReaderService.get_by_cpf(data.get("cpf")):
            flash("CPF já cadastrado", "error")
            return redirect(url_for("leitores.cadastrar_leitores"))

        valid_fields = ["nome", "cpf", "data_nascimento", "email", "telefone", "cep",
                         "logradouro", "bairro", "cidade", "uf", "numero_endereco",
                           "numero_matricula", "limite_emprestimo", "observacao", 
                           "status", "obs_interna", "foto"]
        
        reader_data = {k: v for k, v in data.items() if k in valid_fields}
        reader = ReaderService.create(**reader_data)

        flash("Leitor salvo com sucesso", "success")
        return redirect(url_for("leitores.cadastrar_leitores"))



    return render_template("leitor/leitor.html")


@reader_bp.route("/leitores/<int:id>/delete", methods=["POST"])
def deletar_leitor(id):
    reader = ReaderService.delete(id)
    if not reader:
        flash("Leitor não encontrado", "error")
        return redirect(url_for("leitores.listar_leitores"))
    
    flash("Leitor deletado com sucesso", "success")
    return redirect(url_for("leitores.listar_leitores"))

@reader_bp.route("/leitores/<int:id>/edit", methods=["GET", "POST"])
def editar_leitor(id):
    reader = ReaderService.get_by_id(id)
    if not reader:
        flash("Leitor não encontrado", "error")
        return redirect(url_for("leitores.listar_leitores"))    
    
    if request.method == "POST":
        data = request.form.to_dict()
        foto = request.files.get("foto")
        
        if data.get("data_nascimento"):
            data["data_nascimento"] = datetime.strptime(
                data["data_nascimento"], "%Y-%m-%d").date()

        if foto:
            data["foto"] = ServiceImage.salvar_image(foto, "leitores")

        valid_fields = ["nome", "cpf", "data_nascimento", "email", "telefone", "cep",
                         "logradouro", "bairro", "cidade", "uf", "numero_endereco",
                           "numero_matricula", "limite_emprestimo", "observacao", 
                           "status", "obs_interna", "foto"]
        
        reader_data = {k: v for k, v in data.items() if k in valid_fields}
        updated_reader = ReaderService.update(id, **reader_data)

        flash("Leitor atualizado com sucesso", "success")
        return redirect(url_for("leitores.listar_leitores"))

    return render_template("leitor/leitor.html", show_back_button=True, back_url= url_for('leitores.listar_leitores'), leitor=reader)
                                      

@reader_bp.route("/leitores", methods=["GET"])
def listar_leitores(): 
    lista_de_leitores = ReaderService.get_all()
    
    return render_template("leitor/lista_leitores.html", leitores=lista_de_leitores)