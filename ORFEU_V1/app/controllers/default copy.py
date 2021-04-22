from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from app import app, db, login_manager
from datetime import timedelta

from app.models.tables import Usuario, Categoria, Marca, Medida, Produto
from app.models.forms import LoginForm


@login_manager.user_loader
def get_user(user_id):
    return Usuario.query.filter_by(id=user_id).first()


#  A linha abaixo direciona o usuário para tela de login, caso ele não tenha logado, ou seja, tenha tentado acessar o conteúdo diretamente.
login_manager.login_view = "login"
# A linha abaixo nos permite personalizar a mensagem que o usuário receberá após tentar acessar uma página privada sem logar
login_manager.login_message = u"Você precisa logar para acessar o conteúdo da página!"


login_manager.session_protection = "strong"

# Preciso colocar outro conteúdo na página index.


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(
            nome_usuario=form.nome_usuario.data).first()
        if usuario and usuario.verify_password(form.senha_usuario.data):
            if form.lembrar_me.data:
                login_user(usuario, remember=True, duration=timedelta(days=2))
            else:
                login_user(usuario)
            if usuario.nivel_acesso == "adm":
                return redirect(url_for('adm.index'))
            else:
                return redirect(url_for('op_caixa'))
        else:
            flash("Dados inválidos!")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/op_caixa")
@login_required
def op_caixa():
    return render_template('op_caixa.html')


@app.route("/produtos_cadastrados")
@login_required
def produtos_cadastrados():
    produtos = Produto.query.all()
    return render_template("produtos_cadastrados.html", produtos=produtos)


@app.route("/add_produto", methods=['GET', 'POST'])
@login_required
def add_produto():
    if request.method == 'POST':
        produtos = Produto.query.all()
        for p in produtos:
            if p.codigo == request.form['codigo']:
                return redirect(url_for('index'))
        produto = Produto(request.form['codigo'], request.form['nome_produto'],
                          str(request.form['valor']).replace(",", "."),
                          request.form['quantidade'], request.form['categoria'])
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('produtos_cadastrados'))
    return render_template('add_produto.html')


@app.route("/edit_produto/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_produto(id):
    produto = Produto.query.get(id)
    if request.method == 'POST':
        produto.codigo = request.form['codigo']
        produto.nome_produto = request.form['nome_produto']
        produto.valor = str(request.form['valor']).replace(",", ".")
        produto.quantidade = request.form['quantidade']
        produto.categoria = request.form['categoria']
        db.session.commit()
        return index()
    return render_template('edit_produto.html', produtos=produto)


@app.route("/deletar_produto/<int:id>")
@login_required
def deletar_produto(id):
    produto = Produto.query.get(id)
    return render_template('deletar_produto.html', produtos=produto)


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('produtos_cadastrados'))


@app.route("/usuarios_cadastrados")
@login_required
def usuarios_cadastrados():
    usuarios = Usuario.query.all()
    return render_template("usuarios_cadastrados.html", usuarios=usuarios)


@app.route("/add_usuario", methods=['GET', 'POST'])
@login_required
def add_usuario():
    if request.method == 'POST':
        usuarios = Usuario.query.all()
        for u in usuarios:
            #  Se o cpf já existir mandar de volta para o index
            if u.cpf == request.form['cpf']:
                return redirect(url_for('index'))
        usuario = Usuario(request.form['nome_usuario'], request.form['senha_usuario'],
                          request.form['nome'],
                          request.form['cpf'], request.form['nivel_acesso'])
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuarios_cadastrados'))
    return render_template('add_usuario.html')


@app.route("/edit_usuario/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_usuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome_usuario = request.form['nome_usuario']
        usuario.senha_usuario = usuario.alter_password(
            request.form['senha_usuario'])
        usuario.nome = request.form['nome']
        usuario.cpf = request.form['cpf']
        usuario.nivel_acesso = request.form['nivel_acesso']
        db.session.commit()
        return usuarios_cadastrados()
    return render_template('edit_usuario.html', usuario=usuario)


@app.route("/deletar_usuario/<int:id>")
@login_required
def deletar_usuario(id):
    usuario = Usuario.query.get(id)
    return render_template('deletar_usuario.html', usuario=usuario)


@app.route("/delete_user/<int:id>")
@login_required
def delete_user(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuarios_cadastrados'))


'''  DESCOMENTAR ESSA PARTE DO CÓDIGO PARA CRIAR O O PRIMEIRO USUÁRIO
@app.route("/teste/<info>")
@app.route("/teste", defaults={"info": None})
def teste(info):
    teste_ = Usuario('marcio', '007', 'Marcio', '09419076432', 'adm')
    db.session.add(teste_)
    db.session.commit()
    return "Ok"
'''


@app.route("/teste")
def teste():
    teste_ = Usuario('marcio', '007', 'Marcio', '09419076432', 'adm')
    db.session.add(teste_)
    db.session.commit()
    return "Ok"

'''
@app.route("/ler_produto/<info>")
@app.route("/ler_produto", defaults={"info": None})
def ler_produto(info):
    # usuario_ = Usuario.query.filter_by(nome_usuario="marcio.teste").all()
    usuario_ = Usuario.query.filter_by(nome_usuario="marcio.teste1").first()
    print(usuario_.senha_usuario)
    return usuario_.senha_usuario
'''


@app.route("/teste_add_categoria")
def teste_add_categoria():
    categoria = Categoria('Grãos')
    db.session.add(categoria)
    db.session.commit()
    return "Ok"


@app.route("/teste_add_marca")
def teste_add_marca():
    marca = Marca('Camil')
    db.session.add(marca)
    db.session.commit()
    return "Ok"


@app.route("/teste_add_medida")
def teste_add_medida():
    medida = Medida('KG')
    db.session.add(medida)
    db.session.commit()
    return "Ok"


@app.route("/teste_add_produto")
def teste_add_produto():
    produto = Produto(30, '01256666', 'Espaguete 007', 60, 20, 250, 1.60, 3.90)
    db.session.add(produto)
    db.session.commit()
    return "Ok"


@app.route("/teste_add_produto_full")
def teste_add_produto_full():
    categoria = Categoria('Bebidas 05')
    db.session.add(categoria)
    db.session.commit()
    # marca = Marca('Camil')
    # db.session.add(marca)
    # medida = Medida('KG')
    # db.session.add(medida)
    produto = Produto('0155567121004', 'Teste Bebida 05', 60, 20, 250, 1.60, 4.50)
    db.session.add(produto)
    db.session.commit()
    return "Ok"

#     produto = Produto(1, '1234567891001', 'Feijão', 100, 50, 250, 5.25, 9.75, 1, 1, 1)
#     produto = Produto(2, '1234567891002', 'Arroz', 120, 50, 300, 2.70, 5.50, 1, 1, 1)
#     produto = Produto(3, '1234567891003', 'Espaguete', 60, 20, 250, 1.60, 3.90)
# select * from categoria;
# select * from marca;
# select * from medida;
# select * from produto;