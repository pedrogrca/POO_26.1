"""Serviço de categorias: CRUD e pesquisa."""
from model.categoria import Categoria
from persistence.categoria_repositorio import CategoriaRepositorio
from service.erros import ErroDeNegocio


class CategoriaService:
    """Operações sobre categorias de eventos."""

    def __init__(self, categorias: CategoriaRepositorio):
        self._categorias = categorias

    def inserir(self, nome: str, descricao: str = "") -> Categoria:
        if not nome:
            raise ErroDeNegocio("O nome da categoria é obrigatório.")
        return self._categorias.inserir(Categoria(nome, descricao))

    def atualizar(self, categoria_id: int, nome: str, descricao: str) -> Categoria:
        categoria = self._obter(categoria_id)
        if not nome:
            raise ErroDeNegocio("O nome da categoria é obrigatório.")
        categoria.nome = nome
        categoria.descricao = descricao
        self._categorias.atualizar(categoria)
        return categoria

    def excluir(self, categoria_id: int) -> None:
        if not self._categorias.excluir(categoria_id):
            raise ErroDeNegocio("Categoria não encontrada.")

    def listar(self) -> list[Categoria]:
        return self._categorias.listar_todos()

    def pesquisar(self, parte: str) -> list[Categoria]:
        return self._categorias.buscar_por_nome(parte)

    def buscar_por_id(self, categoria_id: int) -> Categoria | None:
        return self._categorias.buscar_por_id(categoria_id)

    def _obter(self, categoria_id: int) -> Categoria:
        categoria = self._categorias.buscar_por_id(categoria_id)
        if categoria is None:
            raise ErroDeNegocio("Categoria não encontrada.")
        return categoria
