"""Repositório de usuários."""
from model.usuario import Usuario
from persistence.repositorio_json import RepositorioJson


class UsuarioRepositorio(RepositorioJson):
    """Persiste organizadores e participantes no mesmo arquivo.

    A reconstrução polimórfica é feita por :meth:`Usuario.from_dict`, que
    instancia a subclasse correta conforme o campo ``perfil``.
    """

    def __init__(self, caminho_arquivo: str = "data/usuarios.json"):
        super().__init__(caminho_arquivo, Usuario)

    def buscar_por_login(self, login: str) -> Usuario | None:
        """Localiza um usuário pelo login (usado na autenticação)."""
        for usuario in self.listar_todos():
            if usuario.login == login:
                return usuario
        return None
