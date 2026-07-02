"""Entidade CupomDesconto."""
from datetime import date

from model.entidade_base import EntidadeBase


class CupomDesconto(EntidadeBase):
    """Cupom promocional aplicável a uma inscrição (opcional).

    O desconto é percentual sobre o valor do ingresso e só é válido enquanto
    o cupom estiver ativo e dentro da data de validade.
    """

    def __init__(
        self,
        codigo: str,
        percentual_desconto: float,
        ativo: bool = True,
        validade: date | None = None,
        id: int | None = None,
    ):
        super().__init__(id)
        self._codigo = codigo
        self._percentual_desconto = percentual_desconto
        self._ativo = ativo
        self._validade = validade

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        self._codigo = valor

    @property
    def percentual_desconto(self) -> float:
        return self._percentual_desconto

    @percentual_desconto.setter
    def percentual_desconto(self, valor: float) -> None:
        self._percentual_desconto = valor

    @property
    def ativo(self) -> bool:
        return self._ativo

    @ativo.setter
    def ativo(self, valor: bool) -> None:
        self._ativo = valor

    @property
    def validade(self) -> date | None:
        return self._validade

    @validade.setter
    def validade(self, valor: date | None) -> None:
        self._validade = valor

    def esta_valido(self, data_referencia: date | None = None) -> bool:
        """Indica se o cupom pode ser usado na data informada (hoje por padrão)."""
        if not self._ativo:
            return False
        if self._validade is None:
            return True
        data_referencia = data_referencia or date.today()
        return data_referencia <= self._validade

    def calcular_desconto(self, valor: float) -> float:
        """Retorna o valor (em reais) a ser descontado de ``valor``."""
        return round(valor * (self._percentual_desconto / 100.0), 2)

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "codigo": self._codigo,
            "percentual_desconto": self._percentual_desconto,
            "ativo": self._ativo,
            "validade": self._validade.isoformat() if self._validade else None,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "CupomDesconto":
        validade = dados.get("validade")
        return cls(
            codigo=dados["codigo"],
            percentual_desconto=dados["percentual_desconto"],
            ativo=dados.get("ativo", True),
            validade=date.fromisoformat(validade) if validade else None,
            id=dados.get("id"),
        )

    def __str__(self) -> str:
        return f"[{self._id}] {self._codigo} (-{self._percentual_desconto:.0f}%)"
