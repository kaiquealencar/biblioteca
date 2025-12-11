from flask import Blueprint, request, redirect, render_template, flash, url_for


livros_bp = Blueprint("livros", __name__)


@livros_bp.route("/cadastro-livro")
def cadastrar_livro():
    return render_template("livro/livro.html")