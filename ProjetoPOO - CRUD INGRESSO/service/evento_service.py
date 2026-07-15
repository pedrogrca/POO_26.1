"""Serviço de eventos: CRUD, associação e pesquisa."""
from datetime import datetime

from model.evento import Evento
from persistence.categoria_repositorio import CategoriaRepositorio
from persistence.evento_repositorio import EventoRepositorio
from persistence.local_repositorio import LocalRepositorio
from service.erros import ErroDeNegocio


class EventoService:
    """Operações sobre eventos.

    Ao inserir/atualizar um evento, valida a associação com categoria e local
    (relacionamento um-para-muitos armazenado por ``id``).
    """

    def __init__(
        self,
        eventos: EventoRepositorio,
        categorias: CategoriaRepositorio,
        locais: LocalRepositorio,
    ):
        self._eventos = eventos
        self._categorias = categorias
        self._locais = locais

    def inserir(
        self, titulo: str, descricao: str, data_hora: datetime | None,
        organizador_id: int, categoria_id: int, local_id: int,
    ) -> Evento:
        if not titulo:
            raise ErroDeNegocio("O título do evento é obrigatório.")
        self._validar_associacoes(categoria_id, local_id)
        return self._eventos.inserir(
            Evento(titulo, descricao, data_hora, organizador_id, categoria_id, local_id)
        )

    def atualizar(
        self, evento_id: int, titulo: str, descricao: str,
        data_hora: datetime | None, categoria_id: int, local_id: int,
    ) -> Evento:
        evento = self._obter(evento_id)
        if not titulo:
            raise ErroDeNegocio("O título do evento é obrigatório.")
        self._validar_associacoes(categoria_id, local_id)
        evento.titulo = titulo
        evento.descricao = descricao
        evento.data_hora = data_hora
        evento.categoria_id = categoria_id
        evento.local_id = local_id
        self._eventos.atualizar(evento)
        return evento

    def excluir(self, evento_id: int) -> None:
        if not self._eventos.excluir(evento_id):
            raise ErroDeNegocio("Evento não encontrado.")

    def listar(self) -> list[Evento]:
        return self._eventos.listar_todos()

    def pesquisar(self, parte: str) -> list[Evento]:
        """Pesquisa (listagem parcial) de eventos por parte do título."""
        return self._eventos.buscar_por_titulo(parte)

    def listar_por_categoria(self, categoria_id: int) -> list[Evento]:
        return self._eventos.listar_por_categoria(categoria_id)

    def listar_por_organizador(self, organizador_id: int) -> list[Evento]:
        return self._eventos.listar_por_organizador(organizador_id)

    def buscar_por_id(self, evento_id: int) -> Evento | None:
        return self._eventos.buscar_por_id(evento_id)

    # ------------------------------ interno ----------------------------- #
    def _validar_associacoes(self, categoria_id: int, local_id: int) -> None:
        if self._categorias.buscar_por_id(categoria_id) is None:
            raise ErroDeNegocio(f"Categoria {categoria_id} inexistente.")
        if self._locais.buscar_por_id(local_id) is None:
            raise ErroDeNegocio(f"Local {local_id} inexistente.")

    def _obter(self, evento_id: int) -> Evento:
        evento = self._eventos.buscar_por_id(evento_id)
        if evento is None:
            raise ErroDeNegocio("Evento não encontrado.")
        return evento
