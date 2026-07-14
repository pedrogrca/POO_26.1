"""Repositório de eventos."""
from model.evento import Evento
from persistence.repositorio_json import RepositorioJson


class EventoRepositorio(RepositorioJson):
    def __init__(self, caminho_arquivo: str = "data/eventos.json"):
        super().__init__(caminho_arquivo, Evento)

    def buscar_por_titulo(self, parte: str) -> list[Evento]:
        """Pesquisa eventos cujo título contém ``parte`` (sem diferenciar caixa)."""
        termo = parte.lower()
        return [e for e in self.listar_todos() if termo in e.titulo.lower()]

    def listar_por_categoria(self, categoria_id: int) -> list[Evento]:
        """Associação: retorna os eventos de uma categoria."""
        return [e for e in self.listar_todos() if e.categoria_id == categoria_id]

    def listar_por_organizador(self, organizador_id: int) -> list[Evento]:
        """Associação: retorna os eventos criados por um organizador."""
        return [e for e in self.listar_todos() if e.organizador_id == organizador_id]
