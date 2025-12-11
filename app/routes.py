from flask import Blueprint, request, redirect, render_template, flash

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
       return render_template("index.html")