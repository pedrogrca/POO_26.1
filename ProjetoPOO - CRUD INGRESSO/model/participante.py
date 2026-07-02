"""Perfil de usuário: Participante."""
from model.usuario import Usuario


class Participante(Usuario):
    """Usuário que pesquisa eventos e realiza inscrições (compra ingressos)."""

    def __init__(
        self,
        nome: str,
        email: str,
        login: str,
        senha: str,
        cpf: str = "",
        telefone: str = "",
        ativo: bool = True,
        id: int | None = None,
    ):
        super().__init__(nome, email, login, senha, ativo, id)
        self._cpf = cpf
        self._telefone = telefone

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, valor: str) -> None:
        self._cpf = valor

    @property
    def telefone(self) -> str:
        return self._telefone

    @telefone.setter
    def telefone(self, valor: str) -> None:
        self._telefone = valor

    def perfil(self) -> str:
        return "PARTICIPANTE"

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["cpf"] = self._cpf
        dados["telefone"] = self._telefone
        return dados

    @classmethod
    def from_dict(cls, dados: dict) -> "Participante":
        return cls(
            nome=dados["nome"],
            email=dados["email"],
            login=dados["login"],
            senha=dados["senha"],
            cpf=dados.get("cpf", ""),
            telefone=dados.get("telefone", ""),
            ativo=dados.get("ativo", True),
            id=dados.get("id"),
        )
