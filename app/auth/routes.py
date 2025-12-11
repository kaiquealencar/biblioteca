from flask import Blueprint, request, redirect, render_template, flash, url_for, jsonify
from .services import UserService
from app.models import User
usuario_bp = Blueprint("usuarios", __name__)


@usuario_bp.route("/login")
def login():
   return render_template("auth/login.html")


@usuario_bp.route("/cadastro-usuario", methods=["POST", "GET"])
def cadastro_usuario():
   if request.method == "POST":
      usuario = request.form.get("usuario")
      email = request.form.get("email")
      senha = request.form.get("senha")
      user = UserService.create(usuario, email, senha)      
      flash("Usuário cadastrado com sucesso!")


      return redirect(url_for("usuarios.cadastro_usuario"))
   

   users = User.query.all()   
   return render_template("auth/cadastro.html", users=users)