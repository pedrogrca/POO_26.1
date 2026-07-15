"""Menu de operações do perfil Participante."""
from service.erros import ErroDeNegocio
from view.formatacao import descrever_evento
from view.inscricao_view import InscricaoView
from view.tela_base import TelaBase


class MenuParticipante(TelaBase):
    """Menu do participante: pesquisa de eventos, compra e inscrições."""

    def __init__(self, servicos, usuario):
        self._servicos = servicos
        self._usuario = usuario
        self._inscricoes = InscricaoView(servicos)

    def executar(self) -> None:
        while True:
            self.titulo(f"PARTICIPANTE — {self._usuario.nome}")
            print("1) Pesquisar eventos   2) Eventos por categoria")
            print("3) Comprar ingresso    4) Minhas inscrições / cancelar")
            print("0) Sair (logout)")
            opcao = self.ler("Opção")
            if opcao == "0":
                return
            try:
                if opcao == "1":
                    self._pesquisar_eventos()
                elif opcao == "2":
                    self._eventos_por_categoria()
                elif opcao == "3":
                    self._inscricoes.comprar(self._usuario)
                elif opcao == "4":
                    self._inscricoes.minhas_inscricoes(self._usuario)
                else:
                    self.erro("Opção inválida.")
            except ErroDeNegocio as erro:
                self.erro(str(erro))

    def _pesquisar_eventos(self) -> None:
        self.titulo("PESQUISAR EVENTOS")
        eventos = self._servicos.evento.pesquisar(
            self.ler("Parte do título (Enter para todos)")
        )
        if not eventos:
            self.mensagem("Nenhum evento encontrado.")
        for evento in eventos:
            print("  " + descrever_evento(self._servicos, evento))

    def _eventos_por_categoria(self) -> None:
        self.titulo("EVENTOS POR CATEGORIA")
        categorias = self._servicos.categoria.listar()
        if not categorias:
            self.mensagem("Nenhuma categoria cadastrada.")
            return
        for categoria in categorias:
            print(f"  {categoria}")
        categoria_id = self.ler_int("ID da categoria")
        eventos = self._servicos.evento.listar_por_categoria(categoria_id)
        if not eventos:
            self.mensagem("Nenhum evento nesta categoria.")
        for evento in eventos:
            print("  " + descrever_evento(self._servicos, evento))
