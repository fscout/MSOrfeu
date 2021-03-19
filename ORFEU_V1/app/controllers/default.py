from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from app import app, db, login_manager
from datetime import timedelta
import json

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
                return render_template('admin.html', nivel=usuario.nivel_acesso)
                # return redirect(url_for('adm.index'))
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


@app.route("/op_caixa")
@login_required
def op_caixa():
    return render_template('op_caixa.html')


@app.route("/add_produto", methods=['GET', 'POST'])
@login_required
def add_produto():
    if request.method == 'POST':
        produtos = Produto.query.all()
        for p in produtos:
            # print(type(p.id_medida_id))
            if p.cod_brras == request.form['cod_brras'] or p.descricao_prod == request.form['descricao_prod'] and p.id_marca_id == int(request.form['id_marca']):
                print('Esse código ou produto já existejá existe!!!')
                return redirect(url_for('produtos_cadastrados'))
        produto = Produto(request.form['cod_brras'], request.form['descricao_prod'], request.form['quant_prod'], request.form['quant_min'],
                          request.form['quant_max'], str(request.form['preco_custo']).replace(",", "."), str(request.form['preco_venda']).replace(",", "."), request.form['id_categoria'], request.form['id_marca'], request.form['id_medida'])
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('produtos_cadastrados'))
    return redirect(url_for('add_produto_full'))


@app.route("/edit_produto/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_produto(id):
    produto = Produto.query.get(id)
    if request.method == 'POST':
        produto.cod_brras = request.form['cod_brras']
        produto.descricao_prod = request.form['descricao_prod']
        produto.quant_prod = request.form['quant_prod']
        produto.quant_min = request.form['quant_min']
        produto.quant_max = request.form['quant_max']
        produto.preco_custo = str(
            request.form['preco_custo']).replace(",", ".")
        produto.preco_venda = str(
            request.form['preco_venda']).replace(",", ".")
        db.session.commit()
        return redirect(url_for('produtos_cadastrados'))
    return render_template('edit_produto.html', produtos=produto)


@app.route("/produtos_cadastrados")
@login_required
def produtos_cadastrados():
    produtos = Produto.query.all()
    for p in produtos:
        categoria = Categoria.query.get(p.id_categoria_id)
        marca = Marca.query.get(p.id_marca_id)
        medida = Medida.query.get(p.id_medida_id)
        p.nome_categoria = categoria.categoria_produto
        p.nome_marca = marca.marca_produto
        p.nome_medida = medida.medida_produto
    return render_template("produtos_cadastrados.html", produtos=produtos)


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


@app.route("/add_produto_full")
@login_required
def add_produto_full():
    categorias = Categoria.query.all()
    marcas = Marca.query.all()
    medidas = Medida.query.all()
    return render_template('add_produto.html', categorias=categorias, marcas=marcas, medidas=medidas)


@app.route("/add_categoria", methods=['GET', 'POST'])
@login_required
def add_categoria():
    if request.method == 'POST':
        categorias = Categoria.query.all()
        for c in categorias:
            if c.categoria_produto == request.form['categoria_produto']:
                return redirect(url_for('produtos_cadastrados'))
        categoria = Categoria(request.form['categoria_produto'])
        db.session.add(categoria)
        db.session.commit()
        return render_template('add_produto.html')


@app.route("/add_marca", methods=['GET', 'POST'])
@login_required
def add_marca():
    if request.method == 'POST':
        marcas = Marca.query.all()
        for m in marcas:
            if m.marca_produto == request.form['marca_produto']:
                return redirect(url_for('produtos_cadastrados'))
        marca = Marca(request.form['marca_produto'])
        db.session.add(marca)
        db.session.commit()
        return redirect(url_for('add_produto'))
    return redirect(url_for('add_produto'))


@app.route("/add_medida", methods=['GET', 'POST'])
@login_required
def add_medida():
    if request.method == 'POST':
        medidas = Medida.query.all()
        for m in medidas:
            if m.medida_produto == request.form['medida_produto']:
                return redirect(url_for('produtos_cadastrados'))
        medida = Medida(request.form['medida_produto'])
        db.session.add(medida)
        db.session.commit()
        return redirect(url_for('add_produto'))
    return redirect(url_for('add_produto'))


'''
@app.route("/exibir_categorias")
@login_required
def exibir_categorias():
    categorias = Categoria.query.all()
    return render_template('add_produto.html', categorias=categorias)


@app.route("/categorias_cadastradas")
@login_required
def categorias_cadastradas():
    categorias = Categoria.query.all()
    return render_template('categorias_cadastradas.html', categorias=categorias)


@app.route("/teste_add_categoria")
def teste_add_categoria():
    categoria = Categoria('Teste Categ')
    db.session.add(categoria)
    db.session.commit()
    return "Ok"


@app.route("/teste_add_marca")
def teste_add_marca():
    marca = Marca('Nestle')
    db.session.add(marca)
    db.session.commit()
    return "Ok"


@app.route("/teste_add_medida")
def teste_add_medida():
    medida = Medida('Litro')
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
    produto = Produto('0155567121004', 'Teste Bebida 05',
                      60, 20, 250, 1.60, 4.50)
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
'''

'''  DESCOMENTAR ESSA PARTE DO CÓDIGO PARA CRIAR O O PRIMEIRO USUÁRIO
@app.route("/teste/<info>")
@app.route("/teste", defaults={"info": None})
def teste(info):
    teste_ = Usuario('marcio', '007', 'Marcio', '09419076432', 'adm')
    db.session.add(teste_)
    db.session.commit()
    return "Ok"



@app.route("/teste")
def teste():
    teste_ = Usuario('marcio', '007', 'Marcio', '09419076432', 'adm')
    db.session.add(teste_)
    db.session.commit()
    return "Ok"


@app.route("/ler_produto/<info>")
@app.route("/ler_produto", defaults={"info": None})
def ler_produto(info):
    # usuario_ = Usuario.query.filter_by(nome_usuario="marcio.teste").all()
    usuario_ = Usuario.query.filter_by(nome_usuario="marcio.teste1").first()
    print(usuario_.senha_usuario)
    return usuario_.senha_usuario
'''


# @app.route("/teste")
# def teste():
#     teste_ = Usuario('marcio', '007', 'Marcio', '09419076432', 'adm')
#     db.session.add(teste_)
#     db.session.commit()
#     return "Ok"


# @app.route('/recebe_dados_jquery', methods=['POST'])
# def receive_data():
#     if request.method == 'POST':
#         dados = request.form['meus_dados']
#         print(dados)


@app.route('/testes_v1')
def testes_v1():
    return render_template('testes_v1.html')


@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        return json.dumps({'status': 'OK', 'user': user, 'pass': password})



# @app.route("/add_categoria", methods=['GET', 'POST'])
# @login_required
# def add_categoria():
#     # print("Cheguei na Rota")
#     if request.method == 'POST':
#         # print("Entrei no POST")
#         categorias = Categoria.query.all()
#         for c in categorias:
#             # print('Nome Categoria', c.categoria_produto)
#             if c.categoria_produto == request.form['categoria_produto']:
#                 return redirect(url_for('produtos_cadastrados'))
#         categoria = Categoria(request.form['categoria_produto'])
#         # print("Criei o objeto")
#         db.session.add(categoria)
#         db.session.commit()
#         # print("Informações dos objetos", categoria.categoria_produto)
#         return json.dumps({'status': 'OK', 'categoria_produto': categoria.categoria_produto})





@app.route("/teste/<info>")
@app.route("/teste", defaults={"info": None})
def teste(info):
    teste_ = Usuario('Teste', '007', 'Teste', '159', 'Op. Caixa')
    db.session.add(teste_)
    db.session.commit()
    return "Ok"