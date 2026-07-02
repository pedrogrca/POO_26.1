from models import Cliente, Venda, VendaItem, Avaliacao
from daos import ClienteDAO, ProdutoDAO, VendaDAO, CategoriaDAO, AvaliacaoDAO
import datetime

class View:
    def __init__(self):
        self.cliente_dao = ClienteDAO()
        self.produto_dao = ProdutoDAO()
        self.venda_dao = VendaDAO()
        self.categoria_dao = CategoriaDAO()
        self.avaliacao_dao = AvaliacaoDAO()

    def Cliente_Inserir(self, nome, email, senha, fone):
        id = len(self.cliente_dao.listar()) + 1
        novo = Cliente(id, nome, email, senha, fone)
        self.cliente_dao.inserir(novo)

    def Produto_Listar(self):
        return self.produto_dao.listar()

    def Produto_Reajustar(self, percentual):
        for p in self.produto_dao.listar():
            p.preco += p.preco * (percentual / 100)

    def Autenticar(self, email, senha):
        if email == "admin" and senha == "admin":
            return "ADMIN"
        for c in self.cliente_dao.listar():
            if c.email == email and c.senha == senha:
                return c
        return None

    def Venda_Listar_Todas(self):
        return self.venda_dao.listar()

    def Venda_Listar_Cliente(self, id_cliente):
        return [v for v in self.venda_dao.listar() if v.id_cliente == id_cliente]

    def Avaliacao_Inserir(self, id_prod, id_cli, nota, txt):
        nova = Avaliacao(id_prod, id_cli, nota, txt)
        self.avaliacao_dao.inserir(nova)