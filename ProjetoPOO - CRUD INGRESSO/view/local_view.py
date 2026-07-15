"""Tela de gestão de locais (organizador)."""
from service.erros import ErroDeNegocio
from view.tela_base import TelaBase


class LocalView(TelaBase):
    """Interface de CRUD e pesquisa de locais."""

    def __init__(self, servicos):
        self._servico = servicos.local

    def menu(self) -> None:
        while True:
            self.titulo("LOCAIS")
            print("1) Listar   2) Pesquisar   3) Inserir   4) Editar   5) Excluir   0) Voltar")
            opcao = self.ler("Opção")
            if opcao == "0":
                return
            try:
                acoes = {
                    "1": self._listar, "2": self._pesquisar, "3": self._inserir,
                    "4": self._editar, "5": self._excluir,
                }
                acao = acoes.get(opcao)
                if acao:
                    acao()
                else:
                    self.erro("Opção inválida.")
            except ErroDeNegocio as erro:
                self.erro(str(erro))

    def _exibir(self, local) -> None:
        print(f"  {local} | {local.endereco} | capacidade: {local.capacidade}")

    def _listar(self) -> None:
        locais = self._servico.listar()
        if not locais:
            self.mensagem("Nenhum local cadastrado.")
        for local in locais:
            self._exibir(local)

    def _pesquisar(self) -> None:
        parte = self.ler("Parte do nome")
        encontrados = self._servico.pesquisar(parte)
        if not encontrados:
            self.mensagem("Nenhum local encontrado.")
        for local in encontrados:
            self._exibir(local)

    def _inserir(self) -> None:
        nome = self.ler("Nome", obrigatorio=True)
        endereco = self.ler("Endereço")
        cidade = self.ler("Cidade")
        capacidade = self.ler_int("Capacidade")
        local = self._servico.inserir(nome, endereco, cidade, capacidade)
        self.mensagem(f"Local [{local.id}] cadastrado com sucesso.")

    def _editar(self) -> None:
        local = self._servico.buscar_por_id(self.ler_int("ID do local"))
        if local is None:
            self.erro("Local não encontrado.")
            return
        nome = self.ler(f"Nome [{local.nome}]") or local.nome
        endereco = self.ler(f"Endereço [{local.endereco}]") or local.endereco
        cidade = self.ler(f"Cidade [{local.cidade}]") or local.cidade
        capacidade = self.ler_int(
            f"Capacidade [{local.capacidade}]", permitir_vazio=True, padrao=local.capacidade
        )
        self._servico.atualizar(local.id, nome, endereco, cidade, capacidade)
        self.mensagem("Local atualizado.")

    def _excluir(self) -> None:
        self._servico.excluir(self.ler_int("ID do local"))
        self.mensagem("Local excluído.")
