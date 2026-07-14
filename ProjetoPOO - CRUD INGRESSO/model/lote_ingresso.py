"""Entidade LoteIngresso."""
from model.entidade_base import EntidadeBase


class LoteIngresso(EntidadeBase):
    """Faixa de ingressos de um evento (ex.: Lote 1, Lote 2, VIP).

    Cada lote pertence a um :class:`~model.evento.Evento` e controla o próprio
    preço e a quantidade de vagas disponíveis.
    """

    def __init__(
        self,
        nome: str,
        preco: float,
        quantidade_total: int,
        quantidade_disponivel: int | None = None,
        evento_id: int | None = None,
        id: int | None = None,
    ):
        super().__init__(id)
        self._nome = nome
        self._preco = preco
        self._quantidade_total = quantidade_total
        # Ao criar um lote novo, todas as vagas estão disponíveis.
        self._quantidade_disponivel = (
            quantidade_total if quantidade_disponivel is None else quantidade_disponivel
        )
        self._evento_id = evento_id

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self._nome = valor

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, valor: float) -> None:
        self._preco = valor

    @property
    def quantidade_total(self) -> int:
        return self._quantidade_total

    @quantidade_total.setter
    def quantidade_total(self, valor: int) -> None:
        self._quantidade_total = valor

    @property
    def quantidade_disponivel(self) -> int:
        return self._quantidade_disponivel

    @quantidade_disponivel.setter
    def quantidade_disponivel(self, valor: int) -> None:
        self._quantidade_disponivel = valor

    @property
    def evento_id(self) -> int | None:
        return self._evento_id

    @evento_id.setter
    def evento_id(self, valor: int | None) -> None:
        self._evento_id = valor

    # ------------------------------------------------------------------ #
    # Regras próprias do lote (usadas pela regra de negócio de inscrição)
    # ------------------------------------------------------------------ #
    def ha_disponibilidade(self, qtd: int = 1) -> bool:
        """Indica se há vagas suficientes no lote."""
        return self._quantidade_disponivel >= qtd

    def decrementar(self, qtd: int = 1) -> None:
        """Reduz a quantidade disponível ao efetivar uma inscrição."""
        if not self.ha_disponibilidade(qtd):
            raise ValueError("Não há vagas suficientes neste lote.")
        self._quantidade_disponivel -= qtd

    def incrementar(self, qtd: int = 1) -> None:
        """Devolve vagas ao lote (ex.: cancelamento de inscrição)."""
        novo_total = self._quantidade_disponivel + qtd
        # Não pode ultrapassar a quantidade total do lote.
        self._quantidade_disponivel = min(novo_total, self._quantidade_total)

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "preco": self._preco,
            "quantidade_total": self._quantidade_total,
            "quantidade_disponivel": self._quantidade_disponivel,
            "evento_id": self._evento_id,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "LoteIngresso":
        return cls(
            nome=dados["nome"],
            preco=dados["preco"],
            quantidade_total=dados["quantidade_total"],
            quantidade_disponivel=dados.get("quantidade_disponivel"),
            evento_id=dados.get("evento_id"),
            id=dados.get("id"),
        )

    def __str__(self) -> str:
        return (
            f"[{self._id}] {self._nome} - R$ {self._preco:.2f} "
            f"({self._quantidade_disponivel}/{self._quantidade_total} vagas)"
        )
