from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Pessoa(db.Model):
    __tablename__ = 'pessoas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Armazenar o encoding facial como texto ou binário (JSON/pickle)
    encoding_facial = db.Column(db.Text, nullable=True) 

    # Relacionamentos
    imagens = db.relationship('Imagem', backref='pessoa', lazy=True, cascade="all, delete-orphan")
    historico = db.relationship('HistoricoReconhecimento', backref='pessoa', lazy=True, cascade="all, delete-orphan")

class Imagem(db.Model):
    __tablename__ = 'imagens'
    
    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    caminho_imagem = db.Column(db.String(255), nullable=False)

class HistoricoReconhecimento(db.Model):
    __tablename__ = 'historico_reconhecimento'
    
    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    confianca = db.Column(db.Float, nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    origem = db.Column(db.String(50), nullable=False) # 'webcam' ou 'upload'
