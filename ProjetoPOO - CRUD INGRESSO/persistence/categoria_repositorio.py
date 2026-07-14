"""Repositório de categorias."""
from model.categoria import Categoria
from persistence.repositorio_json import RepositorioJson


class CategoriaRepositorio(RepositorioJson):
    def __init__(self, caminho_arquivo: str = "data/categorias.json"):
        super().__init__(caminho_arquivo, Categoria)

    def buscar_por_nome(self, parte: str) -> list[Categoria]:
        """Pesquisa categorias cujo nome contém ``parte`` (sem diferenciar caixa)."""
        termo = parte.lower()
        return [c for c in self.listar_todos() if termo in c.nome.lower()]
