"""Tela de gestão de categorias (organizador)."""
from service.erros import ErroDeNegocio
from view.tela_base import TelaBase


class CategoriaView(TelaBase):
    """Interface de CRUD e pesquisa de categorias."""

    def __init__(self, servicos):
        self._servico = servicos.categoria

    def menu(self) -> None:
        while True:
            self.titulo("CATEGORIAS")
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

    def _exibir(self, categoria) -> None:
        print(f"  {categoria} - {categoria.descricao}")

    def _listar(self) -> None:
        categorias = self._servico.listar()
        if not categorias:
            self.mensagem("Nenhuma categoria cadastrada.")
        for categoria in categorias:
            self._exibir(categoria)

    def _pesquisar(self) -> None:
        parte = self.ler("Parte do nome")
        encontrados = self._servico.pesquisar(parte)
        if not encontrados:
            self.mensagem("Nenhuma categoria encontrada.")
        for categoria in encontrados:
            self._exibir(categoria)

    def _inserir(self) -> None:
        nome = self.ler("Nome", obrigatorio=True)
        descricao = self.ler("Descrição")
        categoria = self._servico.inserir(nome, descricao)
        self.mensagem(f"Categoria [{categoria.id}] cadastrada com sucesso.")

    def _editar(self) -> None:
        categoria = self._servico.buscar_por_id(self.ler_int("ID da categoria"))
        if categoria is None:
            self.erro("Categoria não encontrada.")
            return
        nome = self.ler(f"Nome [{categoria.nome}]") or categoria.nome
        descricao = self.ler(f"Descrição [{categoria.descricao}]") or categoria.descricao
        self._servico.atualizar(categoria.id, nome, descricao)
        self.mensagem("Categoria atualizada.")

    def _excluir(self) -> None:
        self._servico.excluir(self.ler_int("ID da categoria"))
        self.mensagem("Categoria excluída.")
