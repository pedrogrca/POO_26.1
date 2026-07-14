"""Menu de terminal do GestEventos. Execute: python main.py"""
from datetime import date, datetime
import sys
import uuid

from model.categoria import Categoria
from model.cupom_desconto import CupomDesconto
from model.evento import Evento
from model.inscricao import Inscricao
from model.local import Local
from model.lote_ingresso import LoteIngresso
from model.organizador import Organizador
from model.pagamento import Pagamento
from model.participante import Participante
from persistence.categoria_repositorio import CategoriaRepositorio
from persistence.cupom_desconto_repositorio import CupomDescontoRepositorio
from persistence.evento_repositorio import EventoRepositorio
from persistence.inscricao_repositorio import InscricaoRepositorio
from persistence.local_repositorio import LocalRepositorio
from persistence.lote_ingresso_repositorio import LoteIngressoRepositorio
from persistence.pagamento_repositorio import PagamentoRepositorio
from persistence.usuario_repositorio import UsuarioRepositorio

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class Sistema:
    def __init__(self):
        self.usuarios = UsuarioRepositorio()
        self.categorias = CategoriaRepositorio()
        self.locais = LocalRepositorio()
        self.eventos = EventoRepositorio()
        self.lotes = LoteIngressoRepositorio()
        self.cupons = CupomDescontoRepositorio()
        self.inscricoes = InscricaoRepositorio()
        self.pagamentos = PagamentoRepositorio()
        self.usuario = None

    @staticmethod
    def titulo(texto):
        print("\n" + "=" * 55 + f"\n {texto}\n" + "=" * 55)

    @staticmethod
    def ler_int(mensagem):
        return int(input(mensagem).strip())

    def carregar_demo(self):
        if self.usuarios.buscar_por_login("admin"):
            print("Dados de demonstração já existem.")
            return
        org = self.usuarios.inserir(Organizador("Administrador", "admin@gesteventos.com", "admin", "admin", "IFRN"))
        self.usuarios.inserir(Participante("Maria Silva", "maria@email.com", "maria", "123", "000.000.000-00", "99999-0000"))
        categoria = self.categorias.inserir(Categoria("Tecnologia", "Eventos de tecnologia"))
        local = self.locais.inserir(Local("Auditório Central", "Av. Salgado Filho", "Natal", 300))
        evento = self.eventos.inserir(Evento("TechConf 2026", "Conferência de tecnologia", datetime(2026, 9, 15, 19, 30), org.id, categoria.id, local.id))
        self.lotes.inserir(LoteIngresso("Lote 1", 80.0, 100, evento_id=evento.id))
        self.lotes.inserir(LoteIngresso("VIP", 200.0, 20, evento_id=evento.id))
        self.cupons.inserir(CupomDesconto("PROMO10", 10.0, validade=date(2027, 12, 31)))
        print("Dados criados. Organizador: admin/admin | Participante: maria/123")

    def listar_eventos(self):
        termo = input("Pesquisar por título (Enter para todos): ").strip()
        eventos = self.eventos.buscar_por_titulo(termo)
        if not eventos:
            print("Nenhum evento encontrado.")
        for evento in eventos:
            categoria = self.categorias.buscar_por_id(evento.categoria_id)
            local = self.locais.buscar_por_id(evento.local_id)
            print(f"{evento} | Categoria: {categoria.nome if categoria else '-'} | Local: {local.nome if local else '-'}")

    def cadastrar_participante(self):
        self.titulo("CADASTRO DE PARTICIPANTE")
        nome, email = input("Nome: "), input("E-mail: ")
        login, senha = input("Login: "), input("Senha: ")
        if self.usuarios.buscar_por_login(login):
            print("Login já cadastrado."); return
        participante = Participante(nome, email, login, senha, input("CPF: "), input("Telefone: "))
        self.usuarios.inserir(participante)
        print("Participante cadastrado com sucesso.")

    def login(self):
        login, senha = input("Login: "), input("Senha: ")
        usuario = self.usuarios.buscar_por_login(login)
        if not usuario or not usuario.verificar_senha(senha):
            print("Login ou senha inválidos."); return
        self.usuario = usuario
        (self.menu_organizador if usuario.perfil() == "ORGANIZADOR" else self.menu_participante)()

    def crud_categoria(self):
        while True:
            self.titulo("CATEGORIAS")
            print("1 Listar | 2 Inserir | 3 Editar | 4 Excluir | 0 Voltar")
            op = input("> ")
            if op == "0": return
            if op == "1":
                for x in self.categorias.listar_todos(): print(f"{x} - {x.descricao}")
            elif op == "2": self.categorias.inserir(Categoria(input("Nome: "), input("Descrição: ")))
            elif op == "3":
                x = self.categorias.buscar_por_id(self.ler_int("ID: "))
                if x: x.nome, x.descricao = input(f"Nome [{x.nome}]: ") or x.nome, input(f"Descrição [{x.descricao}]: ") or x.descricao; self.categorias.atualizar(x)
            elif op == "4": print("Excluído." if self.categorias.excluir(self.ler_int("ID: ")) else "ID não encontrado.")

    def crud_local(self):
        while True:
            self.titulo("LOCAIS")
            print("1 Listar | 2 Inserir | 3 Editar | 4 Excluir | 0 Voltar")
            op = input("> ")
            if op == "0": return
            if op == "1":
                for x in self.locais.listar_todos(): print(f"{x} | {x.endereco} | capacidade: {x.capacidade}")
            elif op == "2": self.locais.inserir(Local(input("Nome: "), input("Endereço: "), input("Cidade: "), self.ler_int("Capacidade: ")))
            elif op == "3":
                x=self.locais.buscar_por_id(self.ler_int("ID: "))
                if x:
                    x.nome=input(f"Nome [{x.nome}]: ") or x.nome; x.endereco=input(f"Endereço [{x.endereco}]: ") or x.endereco; x.cidade=input(f"Cidade [{x.cidade}]: ") or x.cidade
                    capacidade=input(f"Capacidade [{x.capacidade}]: "); x.capacidade=int(capacidade) if capacidade else x.capacidade; self.locais.atualizar(x)
            elif op == "4": print("Excluído." if self.locais.excluir(self.ler_int("ID: ")) else "ID não encontrado.")

    def crud_evento(self):
        while True:
            self.titulo("EVENTOS")
            print("1 Listar/pesquisar | 2 Inserir | 3 Editar | 4 Excluir | 0 Voltar")
            op=input("> ")
            if op == "0": return
            if op == "1": self.listar_eventos()
            elif op in ("2", "3"):
                antigo = self.eventos.buscar_por_id(self.ler_int("ID do evento: ")) if op == "3" else None
                if op == "3" and not antigo: print("ID não encontrado."); continue
                try:
                    titulo=input(f"Título [{antigo.titulo}]: ") if antigo else input("Título: "); titulo=titulo or antigo.titulo
                    descricao=input(f"Descrição [{antigo.descricao}]: ") if antigo else input("Descrição: "); descricao=descricao or antigo.descricao
                    data=input("Data/hora (dd/mm/aaaa hh:mm): "); data=datetime.strptime(data, "%d/%m/%Y %H:%M") if data else antigo.data_hora
                    categoria=self.ler_int("ID da categoria: ") if not antigo else int(input(f"ID categoria [{antigo.categoria_id}]: ") or antigo.categoria_id)
                    local=self.ler_int("ID do local: ") if not antigo else int(input(f"ID local [{antigo.local_id}]: ") or antigo.local_id)
                    if not self.categorias.buscar_por_id(categoria) or not self.locais.buscar_por_id(local): raise ValueError("Categoria/local inválido.")
                    novo=Evento(titulo, descricao, data, self.usuario.id, categoria, local, id=antigo.id if antigo else None)
                    self.eventos.atualizar(novo) if antigo else self.eventos.inserir(novo)
                except ValueError as e: print(f"Erro: {e}")
            elif op == "4": print("Excluído." if self.eventos.excluir(self.ler_int("ID: ")) else "ID não encontrado.")

    def crud_lote(self):
        while True:
            self.titulo("LOTES DE INGRESSO")
            print("1 Listar | 2 Inserir | 3 Editar | 4 Excluir | 0 Voltar")
            op=input("> ")
            if op == "0": return
            if op == "1":
                for x in self.lotes.listar_todos(): print(x)
            elif op in ("2", "3"):
                antigo=self.lotes.buscar_por_id(self.ler_int("ID do lote: ")) if op == "3" else None
                if op == "3" and not antigo: print("ID não encontrado."); continue
                nome=input(f"Nome [{antigo.nome}]: ") if antigo else input("Nome: "); nome=nome or antigo.nome
                preco=input(f"Preço [{antigo.preco}]: ") if antigo else input("Preço: "); preco=float(preco or antigo.preco)
                total=input(f"Quantidade [{antigo.quantidade_total}]: ") if antigo else input("Quantidade: "); total=int(total or antigo.quantidade_total)
                evento=input(f"ID evento [{antigo.evento_id}]: ") if antigo else input("ID evento: "); evento=int(evento or antigo.evento_id)
                if not self.eventos.buscar_por_id(evento): print("Evento inválido."); continue
                disponivel=min(antigo.quantidade_disponivel,total) if antigo else total
                novo=LoteIngresso(nome, preco, total, disponivel, evento, id=antigo.id if antigo else None)
                self.lotes.atualizar(novo) if antigo else self.lotes.inserir(novo)
            elif op == "4": print("Excluído." if self.lotes.excluir(self.ler_int("ID: ")) else "ID não encontrado.")

    def crud_cupom(self):
        while True:
            self.titulo("CUPONS")
            print("1 Listar | 2 Inserir | 3 Editar | 4 Excluir | 0 Voltar")
            op=input("> ")
            if op == "0": return
            if op == "1":
                for x in self.cupons.listar_todos(): print(x, "válido" if x.esta_valido() else "inválido")
            elif op in ("2", "3"):
                antigo=self.cupons.buscar_por_id(self.ler_int("ID do cupom: ")) if op == "3" else None
                if op == "3" and not antigo: print("ID não encontrado."); continue
                codigo=input(f"Código [{antigo.codigo}]: ") if antigo else input("Código: "); codigo=(codigo or antigo.codigo).upper()
                percentual=input(f"Percentual [{antigo.percentual_desconto}]: ") if antigo else input("Percentual: "); percentual=float(percentual or antigo.percentual_desconto)
                validade=input("Validade aaaa-mm-dd (vazio sem prazo): "); validade=date.fromisoformat(validade) if validade else (antigo.validade if antigo else None)
                novo=CupomDesconto(codigo, percentual, True, validade, id=antigo.id if antigo else None)
                self.cupons.atualizar(novo) if antigo else self.cupons.inserir(novo)
            elif op == "4": print("Excluído." if self.cupons.excluir(self.ler_int("ID: ")) else "ID não encontrado.")

    def comprar(self):
        self.listar_eventos()
        evento_id=self.ler_int("ID do evento: ")
        lotes=self.lotes.listar_por_evento(evento_id)
        for lote in lotes: print(lote)
        lote=self.lotes.buscar_por_id(self.ler_int("ID do lote: "))
        if not lote or lote.evento_id != evento_id or not lote.ha_disponibilidade(): print("Lote inválido ou esgotado."); return
        codigo=input("Cupom (Enter se não houver): ").strip()
        cupom=self.cupons.buscar_por_codigo(codigo) if codigo else None
        if codigo and (not cupom or not cupom.esta_valido()): print("Cupom inválido."); return
        desconto=cupom.calcular_desconto(lote.preco) if cupom else 0
        inscricao=self.inscricoes.inserir(Inscricao(uuid.uuid4().hex[:8].upper(), self.usuario.id, lote.id, lote.preco, lote.preco-desconto, cupom.id if cupom else None))
        lote.decrementar(); self.lotes.atualizar(lote)
        forma=input("Forma de pagamento [PIX]: ") or "PIX"; self.pagamentos.inserir(Pagamento(inscricao.id, inscricao.valor_final, forma))
        print(f"Compra confirmada! Código: {inscricao.codigo_ingresso} | Total: R$ {inscricao.valor_final:.2f}")

    def minhas_inscricoes(self):
        itens=self.inscricoes.listar_por_participante(self.usuario.id)
        for x in itens: print(x, "| usado" if x.utilizado else "")
        if input("Cancelar ingresso? (s/N): ").lower() != "s": return
        item=self.inscricoes.buscar_por_id(self.ler_int("ID da inscrição: "))
        if not item or item.participante_id != self.usuario.id or item.status == Inscricao.STATUS_CANCELADA: print("Inscrição inválida."); return
        item.cancelar(); self.inscricoes.atualizar(item)
        lote=self.lotes.buscar_por_id(item.lote_id); lote.incrementar(); self.lotes.atualizar(lote)
        pagamento=self.pagamentos.buscar_por_inscricao(item.id)
        if pagamento: pagamento.estornar(); self.pagamentos.atualizar(pagamento)
        print("Inscrição cancelada, vaga devolvida e pagamento estornado.")

    def checkin(self):
        codigo=input("Código do ingresso: ").strip().upper(); item=self.inscricoes.buscar_por_codigo_ingresso(codigo)
        if not item: print("Ingresso não encontrado.")
        elif item.status == Inscricao.STATUS_CANCELADA: print("Ingresso cancelado.")
        elif item.utilizado: print("Ingresso já utilizado.")
        else: item.utilizado=True; self.inscricoes.atualizar(item); print("Check-in realizado com sucesso!")

    def inscricoes_evento(self):
        evento_id=self.ler_int("ID do evento: "); ids={x.id for x in self.lotes.listar_por_evento(evento_id)}
        for item in self.inscricoes.listar_todos():
            if item.lote_id in ids:
                pessoa=self.usuarios.buscar_por_id(item.participante_id); print(f"{item} | participante: {pessoa.nome if pessoa else '-'}")

    def menu_organizador(self):
        while self.usuario:
            self.titulo(f"ORGANIZADOR: {self.usuario.nome}")
            print("1 Categorias | 2 Locais | 3 Eventos | 4 Lotes | 5 Cupons")
            print("6 Inscrições de um evento | 7 Check-in | 0 Sair")
            op=input("> "); acoes={"1":self.crud_categoria,"2":self.crud_local,"3":self.crud_evento,"4":self.crud_lote,"5":self.crud_cupom,"6":self.inscricoes_evento,"7":self.checkin}
            if op == "0": self.usuario=None
            elif op in acoes: acoes[op]()

    def menu_participante(self):
        while self.usuario:
            self.titulo(f"PARTICIPANTE: {self.usuario.nome}")
            print("1 Pesquisar eventos | 2 Comprar ingresso | 3 Minhas inscrições/cancelar | 0 Sair")
            op=input("> ")
            if op == "0": self.usuario=None
            elif op == "1": self.listar_eventos()
            elif op == "2": self.comprar()
            elif op == "3": self.minhas_inscricoes()

    def executar(self):
        while True:
            self.titulo("GESTEVENTOS")
            print("1 Entrar | 2 Cadastrar participante | 3 Carregar dados de demonstração | 0 Encerrar")
            op=input("> ")
            try:
                if op == "0": print("Até mais!"); return
                if op == "1": self.login()
                elif op == "2": self.cadastrar_participante()
                elif op == "3": self.carregar_demo()
            except (ValueError, TypeError) as erro:
                print(f"Entrada inválida: {erro}")


if __name__ == "__main__":
    Sistema().executar()
