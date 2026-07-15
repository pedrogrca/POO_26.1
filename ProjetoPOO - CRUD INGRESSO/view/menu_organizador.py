"""Menu de operações do perfil Organizador."""
from service.erros import ErroDeNegocio
from view.categoria_view import CategoriaView
from view.cupom_view import CupomView
from view.evento_view import EventoView
from view.inscricao_view import InscricaoView
from view.local_view import LocalView
from view.lote_ingresso_view import LoteIngressoView
from view.tela_base import TelaBase


class MenuOrganizador(TelaBase):
    """Menu do organizador: CRUDs, associações e regras de negócio."""

    def __init__(self, servicos, usuario):
        self._usuario = usuario
        self._categorias = CategoriaView(servicos)
        self._locais = LocalView(servicos)
        self._eventos = EventoView(servicos, usuario)
        self._lotes = LoteIngressoView(servicos)
        self._cupons = CupomView(servicos)
        self._inscricoes = InscricaoView(servicos)

    def executar(self) -> None:
        while True:
            self.titulo(f"ORGANIZADOR — {self._usuario.nome}")
            print("1) Categorias   2) Locais   3) Eventos   4) Lotes   5) Cupons")
            print("6) Inscrições de um evento   7) Validar ingresso (check-in)")
            print("0) Sair (logout)")
            opcao = self.ler("Opção")
            if opcao == "0":
                return
            acoes = {
                "1": self._categorias.menu,
                "2": self._locais.menu,
                "3": self._eventos.menu,
                "4": self._lotes.menu,
                "5": self._cupons.menu,
                "6": self._inscricoes.inscricoes_do_evento,
                "7": self._inscricoes.checkin,
            }
            acao = acoes.get(opcao)
            if acao is None:
                self.erro("Opção inválida.")
                continue
            try:
                acao()
            except ErroDeNegocio as erro:
                self.erro(str(erro))
