"""Serviço de usuários: autenticação e cadastro (controle de login)."""
from model.organizador import Organizador
from model.participante import Participante
from model.usuario import Usuario
from persistence.usuario_repositorio import UsuarioRepositorio
from service.erros import ErroDeNegocio


class UsuarioService:
    """Operações de controle de acesso e cadastro de usuários."""

    def __init__(self, usuarios: UsuarioRepositorio):
        self._usuarios = usuarios

    # --------------------------- autenticação --------------------------- #
    def autenticar(self, login: str, senha: str) -> Usuario:
        """Valida as credenciais e retorna o usuário autenticado."""
        usuario = self._usuarios.buscar_por_login(login)
        if usuario is None or not usuario.verificar_senha(senha):
            raise ErroDeNegocio("Login ou senha inválidos.")
        if not usuario.ativo:
            raise ErroDeNegocio("Usuário inativo. Procure o organizador.")
        return usuario

    # ----------------------------- cadastro ----------------------------- #
    def cadastrar_participante(
        self, nome: str, email: str, login: str, senha: str,
        cpf: str = "", telefone: str = "",
    ) -> Participante:
        self._validar_credenciais(nome, login, senha)
        return self._usuarios.inserir(
            Participante(nome, email, login, senha, cpf, telefone)
        )

    def cadastrar_organizador(
        self, nome: str, email: str, login: str, senha: str, instituicao: str = "",
    ) -> Organizador:
        self._validar_credenciais(nome, login, senha)
        return self._usuarios.inserir(
            Organizador(nome, email, login, senha, instituicao)
        )

    # ----------------------------- consultas ---------------------------- #
    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        return self._usuarios.buscar_por_id(usuario_id)

    def buscar_por_login(self, login: str) -> Usuario | None:
        return self._usuarios.buscar_por_login(login)

    # ------------------------------ interno ----------------------------- #
    def _validar_credenciais(self, nome: str, login: str, senha: str) -> None:
        if not nome or not login or not senha:
            raise ErroDeNegocio("Nome, login e senha são obrigatórios.")
        if self._usuarios.buscar_por_login(login) is not None:
            raise ErroDeNegocio(f"Já existe um usuário com o login '{login}'.")
