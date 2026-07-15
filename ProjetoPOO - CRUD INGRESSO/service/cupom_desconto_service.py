"""Serviço de cupons de desconto: CRUD e pesquisa por código."""
from datetime import date

from model.cupom_desconto import CupomDesconto
from persistence.cupom_desconto_repositorio import CupomDescontoRepositorio
from service.erros import ErroDeNegocio


class CupomDescontoService:
    """Operações sobre cupons de desconto."""

    def __init__(self, cupons: CupomDescontoRepositorio):
        self._cupons = cupons

    def inserir(
        self, codigo: str, percentual: float, validade: date | None = None
    ) -> CupomDesconto:
        codigo = self._normalizar(codigo, percentual)
        if self._cupons.buscar_por_codigo(codigo) is not None:
            raise ErroDeNegocio(f"Já existe um cupom com o código '{codigo}'.")
        return self._cupons.inserir(CupomDesconto(codigo, percentual, True, validade))

    def atualizar(
        self, cupom_id: int, codigo: str, percentual: float,
        ativo: bool, validade: date | None,
    ) -> CupomDesconto:
        cupom = self._obter(cupom_id)
        codigo = self._normalizar(codigo, percentual)
        existente = self._cupons.buscar_por_codigo(codigo)
        if existente is not None and existente.id != cupom_id:
            raise ErroDeNegocio(f"Já existe um cupom com o código '{codigo}'.")
        cupom.codigo = codigo
        cupom.percentual_desconto = percentual
        cupom.ativo = ativo
        cupom.validade = validade
        self._cupons.atualizar(cupom)
        return cupom

    def excluir(self, cupom_id: int) -> None:
        if not self._cupons.excluir(cupom_id):
            raise ErroDeNegocio("Cupom não encontrado.")

    def listar(self) -> list[CupomDesconto]:
        return self._cupons.listar_todos()

    def buscar_por_codigo(self, codigo: str) -> CupomDesconto | None:
        return self._cupons.buscar_por_codigo(codigo.strip().upper())

    def buscar_por_id(self, cupom_id: int) -> CupomDesconto | None:
        return self._cupons.buscar_por_id(cupom_id)

    def _normalizar(self, codigo: str, percentual: float) -> str:
        if not codigo:
            raise ErroDeNegocio("O código do cupom é obrigatório.")
        if not 0 <= percentual <= 100:
            raise ErroDeNegocio("O percentual de desconto deve estar entre 0 e 100.")
        return codigo.strip().upper()

    def _obter(self, cupom_id: int) -> CupomDesconto:
        cupom = self._cupons.buscar_por_id(cupom_id)
        if cupom is None:
            raise ErroDeNegocio("Cupom não encontrado.")
        return cupom
