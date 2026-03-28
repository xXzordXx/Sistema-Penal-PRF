from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    passaporte = db.Column(db.String(50), nullable=False)
    crimes = db.Column(db.Text, nullable=False)
    relatorio = db.Column(db.Text, nullable=False)


class Imagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registro_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(300), nullable=False)
