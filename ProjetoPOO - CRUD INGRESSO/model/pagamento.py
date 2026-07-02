"""Entidade Pagamento."""
from datetime import datetime

from model.entidade_base import EntidadeBase


class Pagamento(EntidadeBase):
    """Pagamento associado a uma inscrição (relação um-para-um)."""

    STATUS_PENDENTE = "PENDENTE"
    STATUS_PAGO = "PAGO"
    STATUS_ESTORNADO = "ESTORNADO"

    def __init__(
        self,
        inscricao_id: int,
        valor: float,
        forma_pagamento: str = "PIX",
        data_pagamento: datetime | None = None,
        status: str = STATUS_PAGO,
        id: int | None = None,
    ):
        super().__init__(id)
        self._inscricao_id = inscricao_id
        self._valor = valor
        self._forma_pagamento = forma_pagamento
        self._data_pagamento = data_pagamento or datetime.now()
        self._status = status

    @property
    def inscricao_id(self) -> int:
        return self._inscricao_id

    @property
    def valor(self) -> float:
        return self._valor

    @property
    def forma_pagamento(self) -> str:
        return self._forma_pagamento

    @forma_pagamento.setter
    def forma_pagamento(self, valor: str) -> None:
        self._forma_pagamento = valor

    @property
    def data_pagamento(self) -> datetime:
        return self._data_pagamento

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, valor: str) -> None:
        self._status = valor

    def estornar(self) -> None:
        self._status = self.STATUS_ESTORNADO

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "inscricao_id": self._inscricao_id,
            "valor": self._valor,
            "forma_pagamento": self._forma_pagamento,
            "data_pagamento": self._data_pagamento.isoformat()
            if self._data_pagamento
            else None,
            "status": self._status,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Pagamento":
        data_pagamento = dados.get("data_pagamento")
        return cls(
            inscricao_id=dados["inscricao_id"],
            valor=dados["valor"],
            forma_pagamento=dados.get("forma_pagamento", "PIX"),
            data_pagamento=datetime.fromisoformat(data_pagamento)
            if data_pagamento
            else None,
            status=dados.get("status", cls.STATUS_PAGO),
            id=dados.get("id"),
        )

    def __str__(self) -> str:
        return f"[{self._id}] R$ {self._valor:.2f} via {self._forma_pagamento} ({self._status})"
