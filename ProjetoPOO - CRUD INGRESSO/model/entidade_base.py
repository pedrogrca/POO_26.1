"""Classe base do modelo."""
from abc import ABC, abstractmethod


class EntidadeBase(ABC):
    """Superclasse abstrata de todas as entidades do modelo.

    Define o identificador único (``id``) e o contrato de serialização
    (``to_dict`` / ``from_dict``) utilizado pela camada de persistência
    para gravar e ler os objetos em arquivos JSON.
    """

    def __init__(self, id: int | None = None):
        self._id = id

    @property
    def id(self) -> int | None:
        return self._id

    @id.setter
    def id(self, valor: int | None) -> None:
        self._id = valor

    @abstractmethod
    def to_dict(self) -> dict:
        """Converte a entidade em um dicionário serializável em JSON."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls, dados: dict) -> "EntidadeBase":
        """Reconstrói a entidade a partir de um dicionário lido do JSON."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id})"
