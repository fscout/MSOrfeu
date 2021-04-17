from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(20), nullable=False, unique=True)
    senha_usuario = db.Column(db.String(128), nullable=False,)
    nome = db.Column(db.String(50), nullable=False,)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    nivel_acesso = db.Column(db.String(20), nullable=False,)

    def __init__(self, nome_usuario, senha_usuario, nome, cpf, nivel_acesso):
        self.nome_usuario = nome_usuario
        self.senha_usuario = generate_password_hash(senha_usuario)
        self.nome = nome
        self.cpf = cpf
        self.nivel_acesso = nivel_acesso

    def verify_password(self, senha):
        return check_password_hash(self.senha_usuario, senha)

    def alter_password(self, senha):
        self.senha_usuario = generate_password_hash(senha)
        return self.senha_usuario

    def __repr__(self):
        return "<User %r>" % self.id


class Categoria(db.Model):  # Herdando da classe Model
    __tablename__ = "categoria"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria_produto = db.Column(db.String(30), nullable=False, unique=True)

    def __init__(self, categoria_produto):
        self.categoria_produto = categoria_produto

    def __repr__(self):
        return "<Categoria %r>" % self.id


class Marca(db.Model):  # Herdando da classe Model
    __tablename__ = "marca"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marca_produto = db.Column(db.String(30), nullable=False, unique=True)

    def __init__(self, marca_produto):
        self.marca_produto = marca_produto

    def __repr__(self):
        return "<Marca %r>" % self.id


class Medida(db.Model):  # Herdando da classe Model
    __tablename__ = "medida"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medida_produto = db.Column(db.String(30), nullable=False, unique=True)

    def __init__(self, medida_produto):
        self.medida_produto = medida_produto

    def __repr__(self):
        return "<Medida %r>" % self.id


class Produto(db.Model):  # Herdando da classe Model
    __tablename__ = "produto"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_brras = db.Column(db.String(13), nullable=False, unique=True)
    descricao_prod = db.Column(db.String(40), nullable=False, unique=True)
    quant_prod = db.Column(db.Integer, nullable=False)
    quant_min = db.Column(db.Integer)
    quant_max = db.Column(db.Integer)
    preco_custo = db.Column(db.Float(2, 0), nullable=False)
    preco_venda = db.Column(db.Float(2, 0), nullable=False)

    id_categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"))
    categoria = db.relationship('Categoria')

    id_marca_id = db.Column(db.Integer, db.ForeignKey("marca.id"))
    marca = db.relationship('Marca')

    id_medida_id = db.Column(db.Integer, db.ForeignKey("medida.id"))
    medida = db.relationship('Medida')

    # Podemos criar uma categoria, marca e medida padrão, apenas para não
    # obrigarmos que seja incluído qualquer um dos três
    def __init__(self, cod_brras, descricao_prod, quant_prod,
                 quant_min, quant_max, preco_custo, preco_venda,
                 id_categoria_id=None, id_marca_id=None, id_medida_id=None):
        self.cod_brras = cod_brras  # Determinar valores padrões
        self.descricao_prod = descricao_prod
        self.quant_prod = quant_prod
        self.quant_min = quant_min
        self.quant_max = quant_max
        self.preco_custo = preco_custo  # Determinar valores padrões
        self.preco_venda = preco_venda  # Determinar valores padrões
        self.id_categoria_id = id_categoria_id
        self.id_marca_id = id_marca_id
        self.id_medida_id = id_medida_id

    def __repr__(self):
        return "<Produto %r>" % self.id 
