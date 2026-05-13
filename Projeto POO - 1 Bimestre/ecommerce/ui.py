from views import View
from models import Venda, VendaItem

class UI:
    def __init__(self):
        self.view = View()
        self.usuario_logado = None
        self.carrinho = []

    def menu_visitante(self):
        print("\n1-Entrar\n2-Abrir Conta\n0-Sair")
        op = input("Opção: ")
        if op == "1": self.login()
        elif op == "2": self.abrir_conta()
        elif op == "0": exit()

    def abrir_conta(self):
        n = input("Nome: "); e = input("Email: ")
        s = input("Senha: "); f = input("Fone: ")
        self.view.Cliente_Inserir(n, e, s, f)

    def login(self):
        e = input("Email: "); s = input("Senha: ")
        res = self.view.Autenticar(e, s)
        if res:
            self.usuario_logado = res
            self.menu_principal()
        else: print("Falha no login.")

    def menu_principal(self):
        while self.usuario_logado:
            if self.usuario_logado == "ADMIN": self.menu_admin()
            else: self.menu_cliente()

    def menu_admin(self):
        print("\nADMIN: 1-Listar Vendas\n2-Reajustar Preços\n3-Sair")
        op = input("Opção: ")
        if op == "1":
            for v in self.view.Venda_Listar_Todas():
                print(f"Venda ID: {v.id} - Total: {v.total}")
        elif op == "2":
            p = float(input("Percentual: "))
            self.view.Produto_Reajustar(p)
        elif op == "3": self.usuario_logado = None

    def menu_cliente(self):
        print("\nCLIENTE: 1-Produtos\n2-Ver Carrinho\n3-Minhas Compras\n4-Avaliar\n5-Sair")
        op = input("Opção: ")
        if op == "1": self.listar_e_adicionar()
        elif op == "2": self.ver_carrinho()
        elif op == "3": self.minhas_compras()
        elif op == "4": self.avaliar_produto()
        elif op == "5": self.usuario_logado = None

    def listar_e_adicionar(self):
        prods = self.view.Produto_Listar()
        for p in prods: print(f"{p.id}: {p.descricao} - R${p.preco} (Estoque: {p.estoque})")
        id_p = int(input("ID para comprar (0 p/ cancelar): "))
        if id_p == 0: return
        qtd = int(input("Quantidade: "))
        
        for item in self.carrinho:
            if item['id'] == id_p:
                item['qtd'] += qtd
                return
        self.carrinho.append({'id': id_p, 'qtd': qtd})

    def ver_carrinho(self):
        total_geral = 0
        for item in self.carrinho:
            p = self.view.produto_dao.buscar_por_id(item['id'])
            sub = p.preco * item['qtd']
            total_geral += sub
            print(f"{p.descricao} | Unit: {p.preco} | Qtd: {item['qtd']} | Total: {sub}")
        print(f"TOTAL CARRINHO: {total_geral}")
        if input("Comprar? (s/n): ") == "s": self.fechar_pedido(total_geral)

    def fechar_pedido(self, total):
        v_id = len(self.view.venda_dao.listar()) + 1
        venda = Venda(v_id, self.usuario_logado.id, "12/05/2024", total)
        for item in self.carrinho:
            p = self.view.produto_dao.buscar_por_id(item['id'])
            venda.itens.append(VendaItem(v_id, p.id, item['qtd'], p.preco))
            p.estoque -= item['qtd']
        self.view.venda_dao.inserir(venda)
        self.carrinho = []
        print("Compra realizada!")

    def minhas_compras(self):
        compras = self.view.Venda_Listar_Cliente(self.usuario_logado.id)
        for c in compras: print(f"ID: {c.id} - Data: {c.data} - Total: {c.total}")

    def avaliar_produto(self):
        id_p = int(input("ID do produto: "))
        nota = int(input("Nota (1-5): "))
        txt = input("Comentário: ")
        self.view.Avaliacao_Inserir(id_p, self.usuario_logado.id, nota, txt)