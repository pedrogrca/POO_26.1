class DAO:
    categorias = []
    produtos = []
    clientes = []
    vendas = []
    avaliacoes = []

class CategoriaDAO:
    def inserir(self, obj): DAO.categorias.append(obj)
    def listar(self): return DAO.categorias

class ProdutoDAO:
    def inserir(self, obj): DAO.produtos.append(obj)
    def listar(self): return DAO.produtos
    def buscar_por_id(self, id):
        return next((p for p in DAO.produtos if p.id == id), None)

class ClienteDAO:
    def inserir(self, obj): DAO.clientes.append(obj)
    def listar(self): return DAO.clientes

class VendaDAO:
    def inserir(self, obj): DAO.vendas.append(obj)
    def listar(self): return DAO.vendas

class AvaliacaoDAO:
    def inserir(self, obj): DAO.avaliacoes.append(obj)
    def listar_por_produto(self, id_produto):
        return [a for a in DAO.avaliacoes if a.id_produto == id_produto]