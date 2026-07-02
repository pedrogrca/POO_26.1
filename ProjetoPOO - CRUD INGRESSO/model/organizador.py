"""Perfil de usuário: Organizador."""
from model.usuario import Usuario


class Organizador(Usuario):
    """Usuário responsável por criar e administrar eventos, lotes e cupons."""

    def __init__(
        self,
        nome: str,
        email: str,
        login: str,
        senha: str,
        instituicao: str = "",
        ativo: bool = True,
        id: int | None = None,
    ):
        super().__init__(nome, email, login, senha, ativo, id)
        self._instituicao = instituicao

    @property
    def instituicao(self) -> str:
        return self._instituicao

    @instituicao.setter
    def instituicao(self, valor: str) -> None:
        self._instituicao = valor

    def perfil(self) -> str:
        return "ORGANIZADOR"

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["instituicao"] = self._instituicao
        return dados

    @classmethod
    def from_dict(cls, dados: dict) -> "Organizador":
        return cls(
            nome=dados["nome"],
            email=dados["email"],
            login=dados["login"],
            senha=dados["senha"],
            instituicao=dados.get("instituicao", ""),
            ativo=dados.get("ativo", True),
            id=dados.get("id"),
        )
