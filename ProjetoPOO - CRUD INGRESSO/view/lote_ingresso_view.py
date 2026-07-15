"""Tela de gestão de lotes de ingresso (organizador)."""
from service.erros import ErroDeNegocio
from view.tela_base import TelaBase


class LoteIngressoView(TelaBase):
    """Interface de CRUD e associação de lotes de ingresso a eventos."""

    def __init__(self, servicos):
        self._servico = servicos.lote

    def menu(self) -> None:
        while True:
            self.titulo("LOTES DE INGRESSO")
            print("1) Listar de um evento   2) Inserir   3) Editar   4) Excluir   0) Voltar")
            opcao = self.ler("Opção")
            if opcao == "0":
                return
            try:
                acoes = {
                    "1": self._listar_por_evento, "2": self._inserir,
                    "3": self._editar, "4": self._excluir,
                }
                acao = acoes.get(opcao)
                if acao:
                    acao()
                else:
                    self.erro("Opção inválida.")
            except ErroDeNegocio as erro:
                self.erro(str(erro))

    def _listar_por_evento(self) -> None:
        evento_id = self.ler_int("ID do evento")
        lotes = self._servico.listar_por_evento(evento_id)
        if not lotes:
            self.mensagem("Nenhum lote para este evento.")
        for lote in lotes:
            print(f"  {lote}")

    def _inserir(self) -> None:
        evento_id = self.ler_int("ID do evento")
        nome = self.ler("Nome do lote", obrigatorio=True)
        preco = self.ler_float("Preço")
        quantidade = self.ler_int("Quantidade total")
        lote = self._servico.inserir(nome, preco, quantidade, evento_id)
        self.mensagem(f"Lote [{lote.id}] cadastrado com sucesso.")

    def _editar(self) -> None:
        lote = self._servico.buscar_por_id(self.ler_int("ID do lote"))
        if lote is None:
            self.erro("Lote não encontrado.")
            return
        nome = self.ler(f"Nome [{lote.nome}]") or lote.nome
        preco = self.ler_float(f"Preço [{lote.preco}]", permitir_vazio=True, padrao=lote.preco)
        quantidade = self.ler_int(
            f"Quantidade total [{lote.quantidade_total}]",
            permitir_vazio=True, padrao=lote.quantidade_total,
        )
        self._servico.atualizar(lote.id, nome, preco, quantidade)
        self.mensagem("Lote atualizado.")

    def _excluir(self) -> None:
        self._servico.excluir(self.ler_int("ID do lote"))
        self.mensagem("Lote excluído.")
