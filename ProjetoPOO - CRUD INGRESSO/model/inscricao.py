"""Entidade Inscricao (venda/geração de ingresso)."""
from datetime import datetime

from model.entidade_base import EntidadeBase


class Inscricao(EntidadeBase):
    """Registro da inscrição de um participante em um lote de ingresso.

    Reúne os relacionamentos com :class:`~model.participante.Participante`,
    :class:`~model.lote_ingresso.LoteIngresso` e, opcionalmente,
    :class:`~model.cupom_desconto.CupomDesconto`, além dos valores calculados
    pela regra de negócio de inscrição.
    """

    STATUS_CONFIRMADA = "CONFIRMADA"
    STATUS_CANCELADA = "CANCELADA"

    def __init__(
        self,
        codigo_ingresso: str,
        participante_id: int,
        lote_id: int,
        valor_original: float,
        valor_final: float,
        cupom_id: int | None = None,
        data_inscricao: datetime | None = None,
        status: str = STATUS_CONFIRMADA,
        utilizado: bool = False,
        id: int | None = None,
    ):
        super().__init__(id)
        self._codigo_ingresso = codigo_ingresso
        self._participante_id = participante_id
        self._lote_id = lote_id
        self._valor_original = valor_original
        self._valor_final = valor_final
        self._cupom_id = cupom_id
        self._data_inscricao = data_inscricao or datetime.now()
        self._status = status
        self._utilizado = utilizado

    @property
    def codigo_ingresso(self) -> str:
        return self._codigo_ingresso

    @property
    def participante_id(self) -> int:
        return self._participante_id

    @property
    def lote_id(self) -> int:
        return self._lote_id

    @property
    def cupom_id(self) -> int | None:
        return self._cupom_id

    @property
    def valor_original(self) -> float:
        return self._valor_original

    @property
    def valor_final(self) -> float:
        return self._valor_final

    @property
    def data_inscricao(self) -> datetime:
        return self._data_inscricao

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, valor: str) -> None:
        self._status = valor

    @property
    def utilizado(self) -> bool:
        return self._utilizado

    @utilizado.setter
    def utilizado(self, valor: bool) -> None:
        self._utilizado = valor

    def cancelar(self) -> None:
        self._status = self.STATUS_CANCELADA

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "codigo_ingresso": self._codigo_ingresso,
            "participante_id": self._participante_id,
            "lote_id": self._lote_id,
            "cupom_id": self._cupom_id,
            "valor_original": self._valor_original,
            "valor_final": self._valor_final,
            "data_inscricao": self._data_inscricao.isoformat()
            if self._data_inscricao
            else None,
            "status": self._status,
            "utilizado": self._utilizado,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Inscricao":
        data_inscricao = dados.get("data_inscricao")
        return cls(
            codigo_ingresso=dados["codigo_ingresso"],
            participante_id=dados["participante_id"],
            lote_id=dados["lote_id"],
            valor_original=dados["valor_original"],
            valor_final=dados["valor_final"],
            cupom_id=dados.get("cupom_id"),
            data_inscricao=datetime.fromisoformat(data_inscricao)
            if data_inscricao
            else None,
            status=dados.get("status", cls.STATUS_CONFIRMADA),
            utilizado=dados.get("utilizado", False),
            id=dados.get("id"),
        )

    def __str__(self) -> str:
        return (
            f"[{self._id}] Ingresso {self._codigo_ingresso} - "
            f"R$ {self._valor_final:.2f} ({self._status})"
        )
