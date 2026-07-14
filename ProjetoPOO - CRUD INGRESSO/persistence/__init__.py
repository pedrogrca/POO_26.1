"""Camada de persistência (repositórios JSON) do GestEventos."""
from persistence.repositorio_json import RepositorioJson
from persistence.usuario_repositorio import UsuarioRepositorio
from persistence.categoria_repositorio import CategoriaRepositorio
from persistence.local_repositorio import LocalRepositorio
from persistence.evento_repositorio import EventoRepositorio
from persistence.lote_ingresso_repositorio import LoteIngressoRepositorio
from persistence.cupom_desconto_repositorio import CupomDescontoRepositorio
from persistence.inscricao_repositorio import InscricaoRepositorio
from persistence.pagamento_repositorio import PagamentoRepositorio

__all__ = [
    "RepositorioJson",
    "UsuarioRepositorio",
    "CategoriaRepositorio",
    "LocalRepositorio",
    "EventoRepositorio",
    "LoteIngressoRepositorio",
    "CupomDescontoRepositorio",
    "InscricaoRepositorio",
    "PagamentoRepositorio",
]
