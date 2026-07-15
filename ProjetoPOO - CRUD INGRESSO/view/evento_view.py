"""Tela de gestão de eventos (organizador)."""
from service.erros import ErroDeNegocio
from view.formatacao import descrever_evento
from view.tela_base import TelaBase


class EventoView(TelaBase):
    """Interface de CRUD, associação e pesquisa de eventos."""

    def __init__(self, servicos, usuario):
        self._servicos = servicos
        self._servico = servicos.evento
        self._usuario = usuario

    def menu(self) -> None:
        while True:
            self.titulo("EVENTOS")
            print("1) Listar/pesquisar   2) Por categoria   3) Inserir")
            print("4) Editar   5) Excluir   0) Voltar")
            opcao = self.ler("Opção")
            if opcao == "0":
                return
            try:
                acoes = {
                    "1": self._pesquisar, "2": self._por_categoria, "3": self._inserir,
                    "4": self._editar, "5": self._excluir,
                }
                acao = acoes.get(opcao)
                if acao:
                    acao()
                else:
                    self.erro("Opção inválida.")
            except ErroDeNegocio as erro:
                self.erro(str(erro))

    def _exibir(self, evento) -> None:
        print("  " + descrever_evento(self._servicos, evento))

    def _pesquisar(self) -> None:
        parte = self.ler("Pesquisar por parte do título (Enter para todos)")
        eventos = self._servico.pesquisar(parte)
        if not eventos:
            self.mensagem("Nenhum evento encontrado.")
        for evento in eventos:
            self._exibir(evento)

    def _por_categoria(self) -> None:
        categoria_id = self.ler_int("ID da categoria")
        eventos = self._servico.listar_por_categoria(categoria_id)
        if not eventos:
            self.mensagem("Nenhum evento nesta categoria.")
        for evento in eventos:
            self._exibir(evento)

    def _inserir(self) -> None:
        titulo = self.ler("Título", obrigatorio=True)
        descricao = self.ler("Descrição")
        data_hora = self.ler_data_hora("Data/hora")
        categoria_id = self.ler_int("ID da categoria")
        local_id = self.ler_int("ID do local")
        evento = self._servico.inserir(
            titulo, descricao, data_hora, self._usuario.id, categoria_id, local_id
        )
        self.mensagem(f"Evento [{evento.id}] cadastrado com sucesso.")

    def _editar(self) -> None:
        evento = self._servico.buscar_por_id(self.ler_int("ID do evento"))
        if evento is None:
            self.erro("Evento não encontrado.")
            return
        titulo = self.ler(f"Título [{evento.titulo}]") or evento.titulo
        descricao = self.ler(f"Descrição [{evento.descricao}]") or evento.descricao
        data_hora = self.ler_data_hora("Nova data/hora (Enter mantém)", padrao=evento.data_hora)
        categoria_id = self.ler_int(
            f"ID categoria [{evento.categoria_id}]", permitir_vazio=True, padrao=evento.categoria_id
        )
        local_id = self.ler_int(
            f"ID local [{evento.local_id}]", permitir_vazio=True, padrao=evento.local_id
        )
        self._servico.atualizar(
            evento.id, titulo, descricao, data_hora, categoria_id, local_id
        )
        self.mensagem("Evento atualizado.")

    def _excluir(self) -> None:
        self._servico.excluir(self.ler_int("ID do evento"))
        self.mensagem("Evento excluído.")
