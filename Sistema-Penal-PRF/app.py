from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "prf_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# MODELOS
# =========================
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


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
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Usuario.query.filter_by(
            username=request.form["user"],
            password=request.form["pass"]
        ).first()

        if user:
            session["user"] = user.username
            return redirect("/")

        flash("Usuário ou senha inválidos.", "error")

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


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
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        r = Registro(
            nome=request.form["nome"],
            passaporte=request.form["passaporte"],
            crimes=request.form["crimes"],
            relatorio=request.form["relatorio"]
        )
        db.session.add(r)
        db.session.commit()

        flash("Registro criado com sucesso.", "success")
        return redirect("/")

    return render_template("novo.html")


# =========================
# CONSULTA
# =========================
@app.route("/consulta")
def consulta():
    if "user" not in session:
        return redirect("/login")

    termo = request.args.get("q", "").strip()

    if termo:
        registros = Registro.query.filter(
            (Registro.nome.contains(termo)) |
            (Registro.passaporte.contains(termo)) |
            (Registro.crimes.contains(termo))
        ).all()
    else:
        registros = Registro.query.all()

    return render_template("consulta.html", registros=registros, termo=termo)


# =========================
# DETALHE DO REGISTRO
# =========================
@app.route("/registro/<int:registro_id>")
def detalhe_registro(registro_id):
    if "user" not in session:
        return redirect("/login")

    registro = Registro.query.get_or_404(registro_id)
    imagens = Imagem.query.filter_by(registro_id=registro.id).all()
    return render_template("detalhe_registro.html", registro=registro, imagens=imagens)


# =========================
# API PARA BOT
# =========================
@app.route("/api/prisao", methods=["POST"])
def api_prisao():
    data = request.json or {}

    r = Registro(
        nome=data.get("nome"),
        passaporte=data.get("passaporte"),
        crimes=data.get("crimes"),
        relatorio=data.get("relatorio")
    )
    db.session.add(r)
    db.session.commit()

    return {"status": "ok"}


# =========================
# INICIALIZAÇÃO
# =========================
with app.app_context():
    db.create_all()

    if not Usuario.query.filter_by(username="admin").first():
        admin = Usuario(
            username="admin",
            password="PJ6x£lj(5Y6)"
        )
        db.session.add(admin)
        db.session.commit()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
