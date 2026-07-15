"""Telas das operações de inscrição (compra, cancelamento, check-in)."""
from service.erros import ErroDeNegocio
from view.formatacao import descrever_evento
from view.tela_base import TelaBase


class InscricaoView(TelaBase):
    """Interface das regras de negócio de inscrição.

    Reúne as operações do participante (comprar ingresso, minhas inscrições) e
    do organizador (check-in, inscrições de um evento).
    """

    def __init__(self, servicos):
        self._servicos = servicos
        self._servico = servicos.inscricao

    # ----------------------------- participante ------------------------- #
    def comprar(self, participante) -> None:
        self.titulo("COMPRAR INGRESSO")
        eventos = self._servicos.evento.pesquisar(
            self.ler("Pesquisar evento por título (Enter para todos)")
        )
        if not eventos:
            self.mensagem("Nenhum evento encontrado.")
            return
        for evento in eventos:
            print("  " + descrever_evento(self._servicos, evento))

        evento_id = self.ler_int("ID do evento")
        lotes = self._servicos.lote.listar_por_evento(evento_id)
        if not lotes:
            self.mensagem("Este evento não possui lotes de ingresso.")
            return
        self.subtitulo("Lotes disponíveis")
        for lote in lotes:
            print(f"  {lote}")

        lote_id = self.ler_int("ID do lote")
        if lote_id not in {lote.id for lote in lotes}:
            raise ErroDeNegocio("O lote informado não pertence a este evento.")
        codigo_cupom = self.ler("Cupom de desconto (Enter se não houver)")
        forma = self.ler("Forma de pagamento [PIX]") or "PIX"

        inscricao, pagamento = self._servico.realizar_inscricao(
            participante.id, lote_id, codigo_cupom or None, forma
        )
        self.mensagem(
            f"Compra confirmada! Ingresso {inscricao.codigo_ingresso} | "
            f"Total R$ {inscricao.valor_final:.2f} | Pagamento: {pagamento.status}"
        )

    def minhas_inscricoes(self, participante) -> None:
        self.titulo("MINHAS INSCRIÇÕES")
        inscricoes = self._servico.listar_por_participante(participante.id)
        if not inscricoes:
            self.mensagem("Você ainda não possui inscrições.")
            return
        for inscricao in inscricoes:
            pagamento = self._servico.buscar_pagamento(inscricao.id)
            marca = "USADO" if inscricao.utilizado else inscricao.status
            print(
                f"  {inscricao} | pagamento: "
                f"{pagamento.status if pagamento else '-'} | {marca}"
            )
        if not self.confirmar("Deseja cancelar alguma inscrição?"):
            return
        inscricao_id = self.ler_int("ID da inscrição a cancelar")
        self._servico.cancelar_inscricao(inscricao_id, participante.id)
        self.mensagem("Inscrição cancelada, vaga devolvida e pagamento estornado.")

    # ------------------------------ organizador ------------------------- #
    def checkin(self) -> None:
        self.titulo("VALIDAR INGRESSO (CHECK-IN)")
        codigo = self.ler("Código do ingresso", obrigatorio=True)
        inscricao = self._servico.validar_ingresso(codigo)
        self.mensagem(f"Check-in realizado! Ingresso {inscricao.codigo_ingresso} validado.")

    def inscricoes_do_evento(self) -> None:
        self.titulo("INSCRIÇÕES DE UM EVENTO")
        evento_id = self.ler_int("ID do evento")
        inscricoes = self._servico.listar_por_evento(evento_id)
        if not inscricoes:
            self.mensagem("Nenhuma inscrição para este evento.")
            return
        for inscricao in inscricoes:
            pessoa = self._servicos.usuario.buscar_por_id(inscricao.participante_id)
            print(f"  {inscricao} | participante: {pessoa.nome if pessoa else '-'}")
