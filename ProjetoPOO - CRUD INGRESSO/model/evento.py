"""Entidade Evento."""
from datetime import datetime

from model.entidade_base import EntidadeBase


class Evento(EntidadeBase):
    """Evento/conferência criado por um organizador.

    Associa-se a uma :class:`~model.categoria.Categoria`, a um
    :class:`~model.local.Local` e ao :class:`~model.organizador.Organizador`
    que o criou (relacionamentos armazenados por chave estrangeira/``id``).
    """

    def __init__(
        self,
        titulo: str,
        descricao: str = "",
        data_hora: datetime | None = None,
        organizador_id: int | None = None,
        categoria_id: int | None = None,
        local_id: int | None = None,
        id: int | None = None,
    ):
        super().__init__(id)
        self._titulo = titulo
        self._descricao = descricao
        self._data_hora = data_hora
        self._organizador_id = organizador_id
        self._categoria_id = categoria_id
        self._local_id = local_id

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        self._titulo = valor

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, valor: str) -> None:
        self._descricao = valor

    @property
    def data_hora(self) -> datetime | None:
        return self._data_hora

    @data_hora.setter
    def data_hora(self, valor: datetime | None) -> None:
        self._data_hora = valor

    @property
    def organizador_id(self) -> int | None:
        return self._organizador_id

    @organizador_id.setter
    def organizador_id(self, valor: int | None) -> None:
        self._organizador_id = valor

    @property
    def categoria_id(self) -> int | None:
        return self._categoria_id

    @categoria_id.setter
    def categoria_id(self, valor: int | None) -> None:
        self._categoria_id = valor

    @property
    def local_id(self) -> int | None:
        return self._local_id

    @local_id.setter
    def local_id(self, valor: int | None) -> None:
        self._local_id = valor

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "titulo": self._titulo,
            "descricao": self._descricao,
            "data_hora": self._data_hora.isoformat() if self._data_hora else None,
            "organizador_id": self._organizador_id,
            "categoria_id": self._categoria_id,
            "local_id": self._local_id,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Evento":
        data_hora = dados.get("data_hora")
        return cls(
            titulo=dados["titulo"],
            descricao=dados.get("descricao", ""),
            data_hora=datetime.fromisoformat(data_hora) if data_hora else None,
            organizador_id=dados.get("organizador_id"),
            categoria_id=dados.get("categoria_id"),
            local_id=dados.get("local_id"),
            id=dados.get("id"),
        )

    def __str__(self) -> str:
        quando = self._data_hora.strftime("%d/%m/%Y %H:%M") if self._data_hora else "s/ data"
        return f"[{self._id}] {self._titulo} ({quando})"
