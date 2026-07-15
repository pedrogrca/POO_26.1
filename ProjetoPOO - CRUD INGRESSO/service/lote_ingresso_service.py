"""Serviço de lotes de ingresso: CRUD e associação ao evento."""
from model.lote_ingresso import LoteIngresso
from persistence.evento_repositorio import EventoRepositorio
from persistence.lote_ingresso_repositorio import LoteIngressoRepositorio
from service.erros import ErroDeNegocio


class LoteIngressoService:
    """Operações sobre lotes de ingresso de um evento."""

    def __init__(
        self, lotes: LoteIngressoRepositorio, eventos: EventoRepositorio
    ):
        self._lotes = lotes
        self._eventos = eventos

    def inserir(
        self, nome: str, preco: float, quantidade_total: int, evento_id: int
    ) -> LoteIngresso:
        self._validar(nome, preco, quantidade_total)
        if self._eventos.buscar_por_id(evento_id) is None:
            raise ErroDeNegocio(f"Evento {evento_id} inexistente.")
        return self._lotes.inserir(
            LoteIngresso(nome, preco, quantidade_total, evento_id=evento_id)
        )

    def atualizar(
        self, lote_id: int, nome: str, preco: float, quantidade_total: int
    ) -> LoteIngresso:
        lote = self._obter(lote_id)
        self._validar(nome, preco, quantidade_total)
        # Preserva a quantidade de ingressos já vendidos ao redimensionar o lote.
        vendidos = lote.quantidade_total - lote.quantidade_disponivel
        if quantidade_total < vendidos:
            raise ErroDeNegocio(
                f"Já foram vendidos {vendidos} ingressos; a quantidade não pode ser menor."
            )
        lote.nome = nome
        lote.preco = preco
        lote.quantidade_total = quantidade_total
        lote.quantidade_disponivel = quantidade_total - vendidos
        self._lotes.atualizar(lote)
        return lote

    def excluir(self, lote_id: int) -> None:
        if not self._lotes.excluir(lote_id):
            raise ErroDeNegocio("Lote não encontrado.")

    def listar_por_evento(self, evento_id: int) -> list[LoteIngresso]:
        return self._lotes.listar_por_evento(evento_id)

    def buscar_por_id(self, lote_id: int) -> LoteIngresso | None:
        return self._lotes.buscar_por_id(lote_id)

    def _validar(self, nome: str, preco: float, quantidade_total: int) -> None:
        if not nome:
            raise ErroDeNegocio("O nome do lote é obrigatório.")
        if preco < 0:
            raise ErroDeNegocio("O preço não pode ser negativo.")
        if quantidade_total <= 0:
            raise ErroDeNegocio("A quantidade total deve ser maior que zero.")

    def _obter(self, lote_id: int) -> LoteIngresso:
        lote = self._lotes.buscar_por_id(lote_id)
        if lote is None:
            raise ErroDeNegocio("Lote não encontrado.")
        return lote
