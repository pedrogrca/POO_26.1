"""Repositório genérico com persistência em arquivo JSON."""
import json
import os

from model.entidade_base import EntidadeBase


class RepositorioJson:
    """Persiste entidades do modelo em um arquivo JSON (uma lista de objetos).

    Fornece as operações de CRUD comuns a todas as entidades. As subclasses
    apenas informam o caminho do arquivo e a classe do modelo correspondente,
    podendo acrescentar consultas específicas (pesquisas e associações).

    A serialização/desserialização usa os métodos ``to_dict`` e ``from_dict``
    definidos em :class:`~model.entidade_base.EntidadeBase`.
    """

    def __init__(self, caminho_arquivo: str, classe: type):
        self._caminho_arquivo = caminho_arquivo
        self._classe = classe
        # Garante que o diretório de dados exista e que o arquivo seja iniciado.
        diretorio = os.path.dirname(caminho_arquivo)
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)
        if not os.path.exists(caminho_arquivo):
            self._salvar_tudo([])

    # ------------------------------------------------------------------ #
    # Acesso ao arquivo (uso interno)
    # ------------------------------------------------------------------ #
    def _carregar_tudo(self) -> list[dict]:
        with open(self._caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def _salvar_tudo(self, registros: list[dict]) -> None:
        with open(self._caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(registros, arquivo, ensure_ascii=False, indent=2)

    def _proximo_id(self) -> int:
        registros = self._carregar_tudo()
        if not registros:
            return 1
        return max(registro["id"] for registro in registros) + 1

    # ------------------------------------------------------------------ #
    # CRUD
    # ------------------------------------------------------------------ #
    def inserir(self, entidade: EntidadeBase) -> EntidadeBase:
        """Insere uma nova entidade, atribuindo-lhe um ``id`` automático."""
        registros = self._carregar_tudo()
        entidade.id = self._proximo_id()
        registros.append(entidade.to_dict())
        self._salvar_tudo(registros)
        return entidade

    def listar_todos(self) -> list[EntidadeBase]:
        """Retorna todas as entidades reconstruídas a partir do arquivo."""
        return [self._classe.from_dict(registro) for registro in self._carregar_tudo()]

    def buscar_por_id(self, id: int) -> EntidadeBase | None:
        """Retorna a entidade com o ``id`` informado, ou ``None``."""
        for registro in self._carregar_tudo():
            if registro["id"] == id:
                return self._classe.from_dict(registro)
        return None

    def atualizar(self, entidade: EntidadeBase) -> bool:
        """Atualiza a entidade existente (mesmo ``id``). Retorna ``True`` se ok."""
        registros = self._carregar_tudo()
        for indice, registro in enumerate(registros):
            if registro["id"] == entidade.id:
                registros[indice] = entidade.to_dict()
                self._salvar_tudo(registros)
                return True
        return False

    def excluir(self, id: int) -> bool:
        """Remove a entidade com o ``id`` informado. Retorna ``True`` se ok."""
        registros = self._carregar_tudo()
        restantes = [registro for registro in registros if registro["id"] != id]
        if len(restantes) == len(registros):
            return False
        self._salvar_tudo(restantes)
        return True
