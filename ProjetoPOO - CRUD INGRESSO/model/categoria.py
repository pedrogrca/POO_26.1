"""Entidade Categoria."""
from model.entidade_base import EntidadeBase


class Categoria(EntidadeBase):
    """Classificação de um evento (ex.: Tecnologia, Música, Educação)."""

    def __init__(self, nome: str, descricao: str = "", id: int | None = None):
        super().__init__(id)
        self._nome = nome
        self._descricao = descricao

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self._nome = valor

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, valor: str) -> None:
        self._descricao = valor

    def to_dict(self) -> dict:
        return {"id": self._id, "nome": self._nome, "descricao": self._descricao}

    @classmethod
    def from_dict(cls, dados: dict) -> "Categoria":
        return cls(
            nome=dados["nome"],
            descricao=dados.get("descricao", ""),
            id=dados.get("id"),
        )

    def __str__(self) -> str:
        return f"[{self._id}] {self._nome}"
