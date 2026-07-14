"""Entidade de controle de usuários (classe base)."""
from abc import abstractmethod

from model.entidade_base import EntidadeBase


class Usuario(EntidadeBase):
    """Usuário do sistema. Classe base abstrata para os perfis existentes.

    As especializações :class:`~model.organizador.Organizador` e
    :class:`~model.participante.Participante` definem o perfil e os atributos
    específicos de cada tipo de usuário.
    """

    def __init__(
        self,
        nome: str,
        email: str,
        login: str,
        senha: str,
        ativo: bool = True,
        id: int | None = None,
    ):
        super().__init__(id)
        self._nome = nome
        self._email = email
        self._login = login
        self._senha = senha
        self._ativo = ativo

    # ------------------------------------------------------------------ #
    # Propriedades (encapsulamento)
    # ------------------------------------------------------------------ #
    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self._nome = valor

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        self._email = valor

    @property
    def login(self) -> str:
        return self._login

    @login.setter
    def login(self, valor: str) -> None:
        self._login = valor

    @property
    def ativo(self) -> bool:
        return self._ativo

    @ativo.setter
    def ativo(self, valor: bool) -> None:
        self._ativo = valor

    # ------------------------------------------------------------------ #
    # Comportamento
    # ------------------------------------------------------------------ #
    @abstractmethod
    def perfil(self) -> str:
        """Retorna o perfil do usuário (ex.: ``"ORGANIZADOR"``)."""
        raise NotImplementedError

    def verificar_senha(self, senha: str) -> bool:
        """Valida a senha informada no login."""
        return self._senha == senha

    # ------------------------------------------------------------------ #
    # Serialização
    # ------------------------------------------------------------------ #
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "perfil": self.perfil(),
            "nome": self._nome,
            "email": self._email,
            "login": self._login,
            "senha": self._senha,
            "ativo": self._ativo,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Usuario":
        """Fábrica polimórfica: instancia a subclasse conforme o ``perfil``.

        Permite que um único repositório de usuários leia e reconstrua tanto
        organizadores quanto participantes a partir do mesmo arquivo JSON.
        """
        # Importações locais para evitar dependência circular.
        from model.organizador import Organizador
        from model.participante import Participante

        perfil = dados.get("perfil")
        if perfil == "ORGANIZADOR":
            return Organizador.from_dict(dados)
        if perfil == "PARTICIPANTE":
            return Participante.from_dict(dados)
        raise ValueError(f"Perfil de usuário desconhecido: {perfil!r}")
