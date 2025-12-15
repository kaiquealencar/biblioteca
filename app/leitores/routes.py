import os 

from flask import Blueprint, request, redirect, render_template, flash, url_for, jsonify
from werkzeug.utils import secure_filename

from .service import ReaderService
from app.service.arquivos_imagem import ServiceImage
from datetime import datetime

reader_bp = Blueprint("leitores", __name__)

@reader_bp.route("/cadastro-leitor", methods=["POST", "GET"])
def cadastrar_leitores():
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
        reader = ReaderService.create(**reader_data)

        flash("Leitor salvo com sucesso", "success")
        return redirect(url_for("leitores.cadastrar_leitores"))



    return render_template("leitor/leitor.html")