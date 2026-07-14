"""Entidade Local."""
from model.entidade_base import EntidadeBase


class Local(EntidadeBase):
    """Local onde um evento acontece."""

    def __init__(
        self,
        nome: str,
        endereco: str = "",
        cidade: str = "",
        capacidade: int = 0,
        id: int | None = None,
    ):
        super().__init__(id)
        self._nome = nome
        self._endereco = endereco
        self._cidade = cidade
        self._capacidade = capacidade

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self._nome = valor

    @property
    def endereco(self) -> str:
        return self._endereco

    @endereco.setter
    def endereco(self, valor: str) -> None:
        self._endereco = valor

    @property
    def cidade(self) -> str:
        return self._cidade

    @cidade.setter
    def cidade(self, valor: str) -> None:
        self._cidade = valor

    @property
    def capacidade(self) -> int:
        return self._capacidade

    @capacidade.setter
    def capacidade(self, valor: int) -> None:
        self._capacidade = valor

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "endereco": self._endereco,
            "cidade": self._cidade,
            "capacidade": self._capacidade,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Local":
        return cls(
            nome=dados["nome"],
            endereco=dados.get("endereco", ""),
            cidade=dados.get("cidade", ""),
            capacidade=dados.get("capacidade", 0),
            id=dados.get("id"),
        )

    def __str__(self) -> str:
        return f"[{self._id}] {self._nome} - {self._cidade}"
