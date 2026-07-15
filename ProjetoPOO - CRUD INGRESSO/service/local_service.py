"""Serviço de locais: CRUD e pesquisa."""
from model.local import Local
from persistence.local_repositorio import LocalRepositorio
from service.erros import ErroDeNegocio


class LocalService:
    """Operações sobre os locais dos eventos."""

    def __init__(self, locais: LocalRepositorio):
        self._locais = locais

    def inserir(self, nome: str, endereco: str, cidade: str, capacidade: int) -> Local:
        self._validar(nome, capacidade)
        return self._locais.inserir(Local(nome, endereco, cidade, capacidade))

    def atualizar(
        self, local_id: int, nome: str, endereco: str, cidade: str, capacidade: int
    ) -> Local:
        local = self._obter(local_id)
        self._validar(nome, capacidade)
        local.nome = nome
        local.endereco = endereco
        local.cidade = cidade
        local.capacidade = capacidade
        self._locais.atualizar(local)
        return local

    def excluir(self, local_id: int) -> None:
        if not self._locais.excluir(local_id):
            raise ErroDeNegocio("Local não encontrado.")

    def listar(self) -> list[Local]:
        return self._locais.listar_todos()

    def pesquisar(self, parte: str) -> list[Local]:
        return self._locais.buscar_por_nome(parte)

    def buscar_por_id(self, local_id: int) -> Local | None:
        return self._locais.buscar_por_id(local_id)

    def _validar(self, nome: str, capacidade: int) -> None:
        if not nome:
            raise ErroDeNegocio("O nome do local é obrigatório.")
        if capacidade < 0:
            raise ErroDeNegocio("A capacidade não pode ser negativa.")

    def _obter(self, local_id: int) -> Local:
        local = self._locais.buscar_por_id(local_id)
        if local is None:
            raise ErroDeNegocio("Local não encontrado.")
        return local
