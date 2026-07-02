class Categoria:
    def __init__(self, id, descricao):
        self.id = id
        self.descricao = descricao

class Produto:
    def __init__(self, id, descricao, preco, estoque, id_categoria):
        self.id = id
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.id_categoria = id_categoria

class Cliente:
    def __init__(self, id, nome, email, senha, fone):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.fone = fone

class Venda:
    def __init__(self, id, id_cliente, data, total):
        self.id = id
        self.id_cliente = id_cliente
        self.data = data
        self.total = total
        self.itens = []

class VendaItem:
    def __init__(self, id_venda, id_produto, quantidade, preco_unitario):
        self.id_venda = id_venda
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

class Avaliacao:
    def __init__(self, id_produto, id_cliente, nota, comentario):
        self.id_produto = id_produto
        self.id_cliente = id_cliente
        self.nota = nota
        self.comentario = comentario