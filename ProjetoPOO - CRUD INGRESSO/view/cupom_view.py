"""Tela de gestão de cupons de desconto (organizador)."""
from service.erros import ErroDeNegocio
from view.tela_base import TelaBase


class CupomView(TelaBase):
    """Interface de CRUD e pesquisa de cupons de desconto."""

    def __init__(self, servicos):
        self._servico = servicos.cupom

    def menu(self) -> None:
        while True:
            self.titulo("CUPONS DE DESCONTO")
            print("1) Listar   2) Buscar por código   3) Inserir   4) Editar   5) Excluir   0) Voltar")
            opcao = self.ler("Opção")
            if opcao == "0":
                return
            try:
                acoes = {
                    "1": self._listar, "2": self._buscar, "3": self._inserir,
                    "4": self._editar, "5": self._excluir,
                }
                acao = acoes.get(opcao)
                if acao:
                    acao()
                else:
                    self.erro("Opção inválida.")
            except ErroDeNegocio as erro:
                self.erro(str(erro))

    def _exibir(self, cupom) -> None:
        situacao = "válido" if cupom.esta_valido() else "inválido/expirado"
        validade = cupom.validade.strftime("%d/%m/%Y") if cupom.validade else "sem prazo"
        print(f"  {cupom} | validade: {validade} | {situacao}")

    def _listar(self) -> None:
        cupons = self._servico.listar()
        if not cupons:
            self.mensagem("Nenhum cupom cadastrado.")
        for cupom in cupons:
            self._exibir(cupom)

    def _buscar(self) -> None:
        codigo = self.ler("Código do cupom", obrigatorio=True)
        cupom = self._servico.buscar_por_codigo(codigo)
        if cupom is None:
            self.mensagem("Cupom não encontrado.")
        else:
            self._exibir(cupom)

    def _inserir(self) -> None:
        codigo = self.ler("Código", obrigatorio=True)
        percentual = self.ler_float("Percentual de desconto (0-100)")
        validade = self.ler_data("Validade")
        cupom = self._servico.inserir(codigo, percentual, validade)
        self.mensagem(f"Cupom [{cupom.id}] cadastrado com sucesso.")

    def _editar(self) -> None:
        cupom = self._servico.buscar_por_id(self.ler_int("ID do cupom"))
        if cupom is None:
            self.erro("Cupom não encontrado.")
            return
        codigo = self.ler(f"Código [{cupom.codigo}]") or cupom.codigo
        percentual = self.ler_float(
            f"Percentual [{cupom.percentual_desconto}]",
            permitir_vazio=True, padrao=cupom.percentual_desconto,
        )
        ativo = self.confirmar("Cupom ativo?")
        validade = self.ler_data("Validade", padrao=cupom.validade)
        self._servico.atualizar(cupom.id, codigo, percentual, ativo, validade)
        self.mensagem("Cupom atualizado.")

    def _excluir(self) -> None:
        self._servico.excluir(self.ler_int("ID do cupom"))
        self.mensagem("Cupom excluído.")
