from flask import Blueprint, request, redirect, render_template, flash, url_for

usuario_bp = Blueprint("usuarios", __name__)


@usuario_bp.route("/login")
def login():
   return render_template("auth/login.html")


@usuario_bp.route("/cadastro-usuario")
def cadastro_usuario():
   return render_template("auth/cadastro.html")