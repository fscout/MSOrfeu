# from app.models.tables import NivelAcesso, Usuario, Categoria, Marca, Medida, Produto

# SELECT * FROM contato
# SELECT * FROM nivel_acesso
# SELECT * FROM usuario
# SELECT * FROM fiado
# SELECT * FROM categoria
# SELECT * FROM marca
# SELECT * FROM medida
# SELECT * FROM produto


# Observações relacionadas ao nível de acesso:

'''
    Deixaremos já criados os dois níveis de acesso (Admin (Id:1) e
    Op. Caixa (Id:2)). O front deve criar um select para que o usuário
    só possa escolher entre um ou outro nível.
'''

# Variáveis com mensagens padrões para diversos cenários
msg_01 = "Nenhum valor foi informado"
msg_02 = "Nenhum valor foi encontrado"

# Função para adicionar Nível de Acesso
def adicionar_nivel(nivel=None):
    if nivel:
        nivel = NivelAcesso(nivel)
        db.session.add(nivel)
        db.session.commit()
        return listar_niveis()
    global msg_01
    return msg_01

# Função para visualizar a lista com os Níveis de Acesso
def listar_niveis():
    niveis = NivelAcesso.query.all()
    if niveis:
        return niveis
    global msg_02
    return msg_02

# Função para visualizar um Níveis de Acesso específico
def exibir_nivel(id=None):
    if id:
        nivel = NivelAcesso.query.get(id)
        if nivel:
            return nivel
        global msg_02
        return msg_02
    global msg_01
    return msg_01


'''
    Testes realizados
'''
# print(listar_niveis())
# print(exibir_nivel(1))
# print(exibir_nivel(2))
# print(exibir_nivel(5))

# def teste_nivel(nivel=None):
#     if nivel:
#         return "OK"
#     global msg_01
#     return msg_01

# print(teste_nivel())

# nivel = NivelAcesso.query.get(1)
# print(nivel.nivel)
# db.session.query(NivelAcesso).filter(NivelAcesso.id == 1).update({'nivel': "Admin"})
# db.session.commit()
# print(nivel.nivel_acesso)
# print("OK")



# Testes de atualização Nível de Acesso

# Testes de deleção Nível de Acesso

'''

**************************************************************************
**************************************************************************
**************************************************************************
**************************************************************************

'''




def adiciona_produto_lista(produto):
    lista_compras.append(produto)

def remove_produto_lista(produto):
    lista_compras.pop(produto) # Verificar se o pop remove objeto ou só variáveis simples

def atualiza_quantidade_produto(produto, quantidade):
    produto.quantidade = quantidade

def exibir_lista(lista_compras):
    

venda = Venda() # 1

detalhe01 = Detalhe_Venda("Feijão", 1, 10.00, venda.id)
adiciona_produto_lista(detalhe01)

detalhe02 = Detalhe_Venda("Arroz", 1, 5.00, venda.id)
adiciona_produto_lista(detalhe02)

lista_compras = []

