"""Repositório de locais."""
from model.local import Local
from persistence.repositorio_json import RepositorioJson


class LocalRepositorio(RepositorioJson):
    def __init__(self, caminho_arquivo: str = "data/locais.json"):
        super().__init__(caminho_arquivo, Local)

    def buscar_por_nome(self, parte: str) -> list[Local]:
        """Pesquisa locais cujo nome contém ``parte`` (sem diferenciar caixa)."""
        termo = parte.lower()
        return [l for l in self.listar_todos() if termo in l.nome.lower()]
