from flask import Blueprint, request, redirect, render_template, flash, url_for, jsonify
from .services import UserService
from app.models import User
usuario_bp = Blueprint("usuarios", __name__)

@usuario_bp.route("/login", methods=["GET", "POST"])
def login():
   if request.method == "POST":
      email = request.form.get("email")
      senha = request.form.get("senha")

      flash("Login com sucesso!", "success")


   return render_template("auth/login.html")


@usuario_bp.route("/cadastrar-usuario", methods=["POST", "GET"])
def cadastrar_usuario():
   if request.method == "POST":
      usuario = request.form.get("usuario")
      email = request.form.get("email")
      senha = request.form.get("senha")
      user = UserService.create(usuario, email, senha)      
      flash("Usuário cadastrado com sucesso!")


      return redirect(url_for("usuarios.cadastrar_usuario"))
   

   users = User.query.all()   
   return render_template("auth/usuario_form.html", users=users)

@usuario_bp.route("/usuario/<int:id>/editar", methods=["GET", "POST"])
def atualizar_usuario(id):
   user = User.query.get(id)

   if not user:
      return redirect(url_for("usuarios.cadastrar_usuario"))
   
   if request.method == "POST":
      usuario = request.form.get("usuario")
      email = request.form.get("email")
      senha = request.form.get("senha")
      user = UserService.update(id, usuario=usuario, email=email, senha=senha)
      return redirect(url_for("usuarios.cadastrar_usuario"))

   return render_template("auth/usuario_form.html", usuario=user, users=User.query.all())

@usuario_bp.route("/usuarios/<int:id>/delete", methods=["POST"])
def deletar_usuario(id):
   delete_user = UserService.delete(id)
   
   if not delete_user:
      flash("Usuário não encontrado ou já excluído.", "error")
   else:
       flash("Usuário excluído com sucesso!")
   
   return redirect(url_for("usuarios.cadastrar_usuario"))
   

   

