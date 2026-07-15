"""Serviço de inscrições: regras de negócio que envolvem várias entidades."""
import uuid

from model.inscricao import Inscricao
from model.pagamento import Pagamento
from persistence.cupom_desconto_repositorio import CupomDescontoRepositorio
from persistence.inscricao_repositorio import InscricaoRepositorio
from persistence.lote_ingresso_repositorio import LoteIngressoRepositorio
from persistence.pagamento_repositorio import PagamentoRepositorio
from service.erros import ErroDeNegocio


class InscricaoService:
    """Regras de negócio de inscrição (compra), cancelamento e check-in.

    A operação :meth:`realizar_inscricao` é a regra de negócio central do
    sistema: manipula, numa mesma transação lógica, as entidades
    ``LoteIngresso`` (baixa de vaga), ``Inscricao`` (geração do ingresso),
    ``CupomDesconto`` (desconto) e ``Pagamento`` (registro do pagamento).
    """

    def __init__(
        self,
        inscricoes: InscricaoRepositorio,
        lotes: LoteIngressoRepositorio,
        cupons: CupomDescontoRepositorio,
        pagamentos: PagamentoRepositorio,
    ):
        self._inscricoes = inscricoes
        self._lotes = lotes
        self._cupons = cupons
        self._pagamentos = pagamentos

    def realizar_inscricao(
        self, participante_id: int, lote_id: int,
        codigo_cupom: str | None = None, forma_pagamento: str = "PIX",
    ) -> tuple[Inscricao, Pagamento]:
        """Efetiva a compra de um ingresso, aplicando cupom e baixando a vaga."""
        lote = self._lotes.buscar_por_id(lote_id)
        if lote is None:
            raise ErroDeNegocio("Lote de ingresso não encontrado.")
        if not lote.ha_disponibilidade():
            raise ErroDeNegocio("Lote esgotado: não há vagas disponíveis.")

        cupom = None
        if codigo_cupom:
            cupom = self._cupons.buscar_por_codigo(codigo_cupom.strip().upper())
            if cupom is None or not cupom.esta_valido():
                raise ErroDeNegocio("Cupom inválido ou expirado.")

        desconto = cupom.calcular_desconto(lote.preco) if cupom else 0.0
        valor_final = round(lote.preco - desconto, 2)
        codigo_ingresso = uuid.uuid4().hex[:8].upper()

        inscricao = self._inscricoes.inserir(
            Inscricao(
                codigo_ingresso, participante_id, lote_id,
                lote.preco, valor_final, cupom.id if cupom else None,
            )
        )
        # Baixa a vaga no lote e registra o pagamento (regra multi-entidade).
        lote.decrementar()
        self._lotes.atualizar(lote)
        pagamento = self._pagamentos.inserir(
            Pagamento(inscricao.id, valor_final, forma_pagamento)
        )
        return inscricao, pagamento

    def cancelar_inscricao(self, inscricao_id: int, participante_id: int) -> Inscricao:
        """Cancela a inscrição, devolve a vaga ao lote e estorna o pagamento."""
        inscricao = self._inscricoes.buscar_por_id(inscricao_id)
        if inscricao is None or inscricao.participante_id != participante_id:
            raise ErroDeNegocio("Inscrição não encontrada.")
        if inscricao.status == Inscricao.STATUS_CANCELADA:
            raise ErroDeNegocio("Esta inscrição já está cancelada.")
        if inscricao.utilizado:
            raise ErroDeNegocio("Ingresso já utilizado (check-in); não pode ser cancelado.")

        inscricao.cancelar()
        self._inscricoes.atualizar(inscricao)

        lote = self._lotes.buscar_por_id(inscricao.lote_id)
        if lote is not None:
            lote.incrementar()
            self._lotes.atualizar(lote)

        pagamento = self._pagamentos.buscar_por_inscricao(inscricao.id)
        if pagamento is not None:
            pagamento.estornar()
            self._pagamentos.atualizar(pagamento)
        return inscricao

    def validar_ingresso(self, codigo_ingresso: str) -> Inscricao:
        """Check-in: marca o ingresso como utilizado após as validações."""
        inscricao = self._inscricoes.buscar_por_codigo_ingresso(
            codigo_ingresso.strip().upper()
        )
        if inscricao is None:
            raise ErroDeNegocio("Ingresso não encontrado.")
        if inscricao.status == Inscricao.STATUS_CANCELADA:
            raise ErroDeNegocio("Ingresso cancelado.")
        if inscricao.utilizado:
            raise ErroDeNegocio("Ingresso já utilizado.")
        inscricao.utilizado = True
        self._inscricoes.atualizar(inscricao)
        return inscricao

    # ----------------------------- consultas ---------------------------- #
    def listar_por_participante(self, participante_id: int) -> list[Inscricao]:
        return self._inscricoes.listar_por_participante(participante_id)

    def listar_por_evento(self, evento_id: int) -> list[Inscricao]:
        """Associação: inscrições de todos os lotes de um evento."""
        ids_lotes = {lote.id for lote in self._lotes.listar_por_evento(evento_id)}
        return [i for i in self._inscricoes.listar_todos() if i.lote_id in ids_lotes]

    def buscar_pagamento(self, inscricao_id: int) -> Pagamento | None:
        return self._pagamentos.buscar_por_inscricao(inscricao_id)
