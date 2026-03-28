from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "prf_secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# =========================
# MODELOS
# =========================
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))


class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    passaporte = db.Column(db.String(50))
    crimes = db.Column(db.Text)
    relatorio = db.Column(db.Text)


class Imagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registro_id = db.Column(db.Integer)
    url = db.Column(db.String(300))


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = Usuario.query.filter_by(
            username=request.form["user"],
            password=request.form["pass"]
        ).first()

        if user:
            session["user"] = user.username
            return redirect("/")
    return render_template("login.html")


# =========================
# HOME
# =========================
@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    registros = Registro.query.all()
    return render_template("index.html", registros=registros)


# =========================
# NOVO REGISTRO
# =========================
@app.route("/novo", methods=["GET","POST"])
def novo():
    if request.method == "POST":
        r = Registro(
            nome=request.form["nome"],
            passaporte=request.form["passaporte"],
            crimes=request.form["crimes"],
            relatorio=request.form["relatorio"]
        )
        db.session.add(r)
        db.session.commit()

        return redirect("/")

    return render_template("novo.html")


# =========================
# API PARA BOT
# =========================
@app.route("/api/prisao", methods=["POST"])
def api_prisao():
    data = request.json

    r = Registro(
        nome=data["nome"],
        passaporte=data["passaporte"],
        crimes=data["crimes"],
        relatorio=data["relatorio"]
    )
    db.session.add(r)
    db.session.commit()

    return {"status": "ok"}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
