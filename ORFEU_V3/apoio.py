<!-- <p class="ocultar nivel">{{current_user.nivel_acesso}}</p>

<div class="container hider" align="center"> -->



    <!-- <script src="{{ url_for('static', filename='js/verifica_acesso.js')}}"></script> -->






















class NivelAcesso(db.Model):  # Herdando da classe Model
    __tablename__ = "nivel_acesso"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nivel_acesso_usuario = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, nivel_acesso_usuario):
        self.nivel_acesso_usuario = nivel_acesso_usuario

    def adicionar_nivel(self):
        # Usar o try
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def atualizar_nivel(id, nivel_acesso_usuario):
        # Usar o try
        db.session.query(NivelAcesso).filter(NivelAcesso.id == id).update(
            {'nivel_acesso_usuario': nivel_acesso_usuario})
        db.session.commit()

    @staticmethod
    def remover_nivel(id):
        # try
        db.session.query(NivelAcesso).filter(NivelAcesso.id == id).delete()
        db.session.commit()

    def exibir_nivel(self):
        return self.nivel_acesso_usuario

    def listar_nivel(self):
        pass

    def __repr__(self):
        return "<NivelAcesso %r>" % self.id


class Usuario(db.Model):  # Herdando da classe Model
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(25), nullable=False, unique=True)
    senha = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    nivel_acesso_id = db.Column(db.Integer, db.ForeignKey("nivel_acesso.id"))
    nivel_acesso = db.relationship('NivelAcesso')

    def __init__(self, login, senha, status, nivel_acesso_id):
        self.nivel_acesso_id = nivel_acesso_id
        self.login = login
        self.senha = senha
        self.status = status












    def adicionar_usuario(self):
        # Usar o try
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def atualizar_usuario(id, login, senha, status):
        # Usar o try
        db.session.query(Usuario).filter(Usuario.id == id).update(
            {'login': login, 'senha': senha, 'status': status})
        db.session.commit()

    @staticmethod
    def remover_usuario(id):
        # try
        db.session.query(Usuario).filter(Usuario.id == id).delete()
        db.session.commit()

    def exibir_usuario(self):
        return self.login, self.senha, self.status

    def listar_usuario(self):
        return self.login

    def __repr__(self):
        return "<Usuario %r>" % self.id
''''''



          <select size="1" name="categorias">
            <option value="0">Selecione...</option>
            {% for c in categorias %}
            <option value={{c.id}}>{{c.categoria}}</option>
            {% endfor %}
          </select>




/***************************************/

add_produto

  {% if msg != '' %}
    <h1>{{msg}}</h1>
  {% endif %}




    <form action="/consultar_1_produto" method="POST">
    <label class="fill2" for="consultar_cod_brras">Consultar Produto</label>
    <input type="text" class="form-control" id="consultar_cod_brras" name="consultar_cod_brras">
    <button type="submit" class="btn btn-primary">Consultar</button>
  </form>

default

@app.route("/consultar_1_produto", methods=['GET', 'POST'])
@login_required
def consultar_1_produto():
    produtos = Produto.query.all()
    if request.method == 'POST':
        for p in produtos:
            if p.cod_brras == request.form['consultar_cod_brras'] or p.descricao_prod == request.form['consultar_cod_brras']:
                return render_template('edit_produto.html', produtos=p)
        # msg = "Não Existe"
        # return render_template('add_produto.html', msg=msg)
        categoria = Categoria.query.get(int(request.form['id_categoria']))
        print(categoria.categoria_produto)





    {% block header %}

    <a href="/"><img src="{{url_for('static', filename='images/logo.jpeg')}}" alt="MS-Orfeu"></a>
    <nav>

        {% if current_user.is_authenticated %}

            
            {% if nivel == "adm" %}
            <li><a class="fill" href="/add_produto_full">Cadastrar Produtos</a></li>
            <li><a class="fill" href="/produtos_cadastrados">Consultar Produtos</a></li>
            <li><a class="fill" href="/add_usuario">Cadastrar Usuários</a></li>
            <li><a class="fill" href="/usuarios_cadastrados">Consultar Usuários</a></li>
                {% else %}
                <li><a class="fill" href="/usuarios_cadastrados">Consultar Usuários</a></li>
            {% endif %}

            <li><a class="fill" href="{{ url_for('logout') }}">Logout</a></li>
            {% else %}
            <li><a class="fill" href="{{ url_for('login') }}">Login</a></li>
        {% endif %}
    </nav>
        
    {% endblock header %}



CREATE DATABASE orfeu;
USE orfeu;

CREATE TABLE Endereco
(
      idEndereco SMALLINT IDENTITY(1,1) PRIMARY KEY
    , cep VARCHAR(9)
    , logradouro VARCHAR(50)
    , numero SMALLINT
    , complemento VARCHAR(20)
    , bairro VARCHAR(30)
    , cidade VARCHAR(30)
    , uf VARCHAR(2)
)

CREATE TABLE Contato
( 
      idContato SMALLINT IDENTITY(1,1) PRIMARY KEY
    , telefoneFixo VARCHAR(12)
    , telefoneCelular VARCHAR(12) NOT NULL
    , email VARCHAR(50)
)

CREATE TABLE Pessoa
(
      idPessoa SMALLINT IDENTITY(1,1) PRIMARY KEY
    , nomePessoa VARCHAR(50) NOT NULL
    , cpf VARCHAR(12) UNIQUE
    , rg VARCHAR(10) UNIQUE
    , idEndereco SMALLINT
    , idContato SMALLINT NOT NULL
    , FOREIGN KEY(idEndereco) REFERENCES Endereco(idEndereco)
    , FOREIGN KEY(idContato) REFERENCES Contato(idContato)
)

CREATE TABLE NivelAcesso
(
      idNivelAcesso TINYINT IDENTITY(1,1) PRIMARY KEY
    , nivelAcesso VARCHAR(12) UNIQUE NOT NULL
)


CREATE TABLE Pessoa_Usuario
(
      idUsuario SMALLINT IDENTITY(1,1) PRIMARY KEY
    , [login] VARCHAR(25) UNIQUE NOT NULL
    , senha VARCHAR(128) NOT NULL
    , statusUsuario BIT DEFAULT 1
    , idPessoa SMALLINT NOT NULL
    , idNivelAcesso TINYINT NOT NULL
    , FOREIGN KEY(idNivelAcesso) REFERENCES NivelAcesso(idNivelAcesso)
    , FOREIGN KEY(idPessoa) REFERENCES Pessoa(idPessoa)
)


CREATE TABLE Pessoa_Fiado
(
      idFiado SMALLINT IDENTITY(1,1) PRIMARY KEY
    , dataPag DATE
    , valorDivida DECIMAL(9,2) DEFAULT 0
    , dataUltimaCompra DATE
    , idPessoa SMALLINT NOT NULL
    , FOREIGN KEY(idPessoa) REFERENCES Pessoa(idPessoa)
)

CREATE TABLE Categoria
(
      idCategoria SMALLINT IDENTITY(1,1) PRIMARY KEY
    , nomeCategoria VARCHAR(30) UNIQUE NOT NULL
)


CREATE TABLE Marca
(
      idMarca SMALLINT IDENTITY(1,1) PRIMARY KEY
    , nomeMarca VARCHAR(30) UNIQUE NOT NULL
)



CREATE TABLE Medida
(
      idMedida SMALLINT IDENTITY(1,1) PRIMARY KEY
    , nomeMedida VARCHAR(30) UNIQUE NOT NULL
)


CREATE TABLE Produto
(
      idProduto INT IDENTITY(1,1) PRIMARY KEY
    , codProd VARCHAR(13) UNIQUE
    , codBarras VARCHAR(13) UNIQUE
    , descricaoProd VARCHAR(40)
    , quantProd SMALLINT
    , quantMin SMALLINT
    , quantMax SMALLINT
    , precoCusto DECIMAL(9,2) NOT NULL
    , precoVenda DECIMAL(9,2) NOT NULL
    , idCategoria SMALLINT
    , idMarca SMALLINT
    , idMedida SMALLINT
    , FOREIGN KEY(idCategoria) REFERENCES Categoria(idCategoria)
    , FOREIGN KEY(idMarca) REFERENCES Marca(idMarca)
    , FOREIGN KEY(idMedida) REFERENCES Medida(idMedida)
)


CREATE TABLE Venda
(
    idVenda INT IDENTITY(1,1) PRIMARY KEY
    , dataVenda DATE
    , idUsuario SMALLINT NOT NULL
    , idFiado SMALLINT NULL
    , FOREIGN KEY(idUsuario) REFERENCES Pessoa_Usuario(idUsuario)
    , FOREIGN KEY(idFiado) REFERENCES Pessoa_Fiado(idFiado)
)

CREATE TABLE Venda_DetalhesVenda
(
    idDetalhesVenda INT IDENTITY(1,1) PRIMARY KEY
    , quantProdVenda SMALLINT NOT NULL
    , valorUnitarioVenda DECIMAL(9,2)
    , idVenda INT NOT NULL
    , idProduto INT NOT NULL
    , FOREIGN KEY(idVenda) REFERENCES Venda(idVenda)
    , FOREIGN KEY(idProduto) REFERENCES Produto(idProduto)
)

CREATE TABLE Venda_TipoPagamento
(
    idTipoPagamento INT IDENTITY(1,1) PRIMARY KEY
    , tipoPagamento VARCHAR(12)
    , idVenda INT NOT NULL
    , FOREIGN KEY(idVenda) REFERENCES Venda(idVenda)
)

SELECT * FROM Endereco;
SELECT * FROM Contato;
SELECT * FROM Pessoa;
SELECT * FROM NivelAcesso;
SELECT * FROM Pessoa_Usuario;
SELECT * FROM Pessoa_Fiado;
SELECT * FROM Categoria;
SELECT * FROM Marca;
SELECT * FROM Medida;
SELECT * FROM Produto;
SELECT * FROM Venda;
SELECT * FROM Venda_DetalhesVenda;
SELECT * FROM Venda_TipoPagamento;


/**********************************************/


{% extends 'base.html' %}


{% block title %}
{{ super() }} - Login
{% endblock title %}
    

{% block main %}

<div class="container" align="center">
    <h1>Login</h1>
    <div class="col-md-6 col-offset-3">
    <form action="" method="POST">
        {{ form.csrf_token }}
        <div class="form-group">
            {{ form.login(class="form-control", placeholder="Seu Usuário")}}
        </div>

        <div class="form-group">
            {{ form.senha(class="form-control", placeholder="Sua Senha")}}
        </div>
        <div class="checkbox">
            <label>
                {{ form.lembrar_me }} Lembrar-me
            </label>

            <button type="submit" class="btn btn-default">Logar</button>
        </div>
    </form>
</div>



      <!-- Button trigger modal -->
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#esqueciSenha">
        Esqueci a senha!
      </button>
    
  <!-- Modal Categoria -->
  <div class="modal fade" id="esqueciSenha" tabindex="-1" role="dialog" aria-labelledby="esqueciSenhaLabel"
  aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="esqueciSenhaLabel">Esqueceu sua senha? Não se preocupe, digite seu e-mail abaixo e te encaminharemos uma senha provisória</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>

      <div class="modal-body">
        <form action="/recuperar_senha_email" method="POST">
          <div class="form-group col-md-4">
            <!-- <label class="fill2" for="email">Digite o seu e-mail:</label> -->
            <input type="email" class="form-control" id="email" name="email" required>
          </div>
          <button type="submit" class="btn btn-primary">Enviar Senha</button>
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Fechar</button>
        </form>
      </div>
</div>
</div>
</div>
</div>
{% endblock main %}
    