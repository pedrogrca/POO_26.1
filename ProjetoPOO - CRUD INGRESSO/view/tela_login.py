"""Tela inicial: autenticação e cadastro (menu público do sistema)."""
from service.erros import ErroDeNegocio
from view.menu_organizador import MenuOrganizador
from view.menu_participante import MenuParticipante
from view.tela_base import TelaBase


class TelaLogin(TelaBase):
    """Ponto de entrada da interface: controla o acesso ao sistema.

    Após autenticar, direciona o usuário ao menu correspondente ao seu perfil
    (organizador ou participante).
    """

    def __init__(self, servicos):
        self._servicos = servicos

    def executar(self) -> None:
        self.titulo("GESTEVENTOS — Sistema de Gestão de Eventos e Ingressos")
        while True:
            print("\n1) Entrar")
            print("2) Cadastrar-se (participante)")
            print("3) Carregar dados de demonstração")
            print("0) Encerrar")
            opcao = self.ler("Opção")
            try:
                if opcao == "0":
                    self.mensagem("Até mais!")
                    return
                elif opcao == "1":
                    self._entrar()
                elif opcao == "2":
                    self._cadastrar()
                elif opcao == "3":
                    self._carregar_demo()
                else:
                    self.erro("Opção inválida.")
            except ErroDeNegocio as erro:
                self.erro(str(erro))
            except EOFError:
                self.mensagem("Encerrando o sistema.")
                return

    def _entrar(self) -> None:
        login = self.ler("Login", obrigatorio=True)
        senha = self.ler("Senha", obrigatorio=True)
        usuario = self._servicos.usuario.autenticar(login, senha)
        self.mensagem(f"Bem-vindo(a), {usuario.nome}! (perfil: {usuario.perfil()})")
        if usuario.perfil() == "ORGANIZADOR":
            MenuOrganizador(self._servicos, usuario).executar()
        else:
            MenuParticipante(self._servicos, usuario).executar()
        self.mensagem(f"Logout de {usuario.nome} realizado.")

    def _cadastrar(self) -> None:
        self.titulo("CADASTRO DE PARTICIPANTE")
        nome = self.ler("Nome", obrigatorio=True)
        email = self.ler("E-mail")
        login = self.ler("Login", obrigatorio=True)
        senha = self.ler("Senha", obrigatorio=True)
        cpf = self.ler("CPF")
        telefone = self.ler("Telefone")
        self._servicos.usuario.cadastrar_participante(
            nome, email, login, senha, cpf, telefone
        )
        self.mensagem("Cadastro realizado com sucesso! Faça login para continuar.")

    def _carregar_demo(self) -> None:
        if self._servicos.carregar_demo():
            self.mensagem("Dados de demonstração criados.")
        else:
            self.mensagem("Os dados de demonstração já existem.")
        self.mensagem("Acessos: organizador 'admin/admin' | participante 'maria/123'.")
