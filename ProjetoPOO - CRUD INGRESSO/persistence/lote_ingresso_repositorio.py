"""Repositório de lotes de ingressos."""
from model.lote_ingresso import LoteIngresso
from persistence.repositorio_json import RepositorioJson


class LoteIngressoRepositorio(RepositorioJson):
    def __init__(self, caminho_arquivo: str = "data/lotes_ingressos.json"):
        super().__init__(caminho_arquivo, LoteIngresso)

    def listar_por_evento(self, evento_id: int) -> list[LoteIngresso]:
        """Associação: retorna os lotes de ingressos de um evento."""
        return [l for l in self.listar_todos() if l.evento_id == evento_id]
