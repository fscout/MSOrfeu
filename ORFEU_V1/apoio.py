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