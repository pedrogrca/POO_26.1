"""Repositório de inscrições (vendas de ingressos)."""
from model.inscricao import Inscricao
from persistence.repositorio_json import RepositorioJson


class InscricaoRepositorio(RepositorioJson):
    def __init__(self, caminho_arquivo: str = "data/inscricoes.json"):
        super().__init__(caminho_arquivo, Inscricao)

    def listar_por_participante(self, participante_id: int) -> list[Inscricao]:
        """Associação: retorna as inscrições de um participante."""
        return [i for i in self.listar_todos() if i.participante_id == participante_id]

    def listar_por_lote(self, lote_id: int) -> list[Inscricao]:
        """Associação: retorna as inscrições de um lote de ingresso."""
        return [i for i in self.listar_todos() if i.lote_id == lote_id]

    def buscar_por_codigo_ingresso(self, codigo: str) -> Inscricao | None:
        """Localiza uma inscrição pelo código do ingresso (usado no check-in)."""
        for inscricao in self.listar_todos():
            if inscricao.codigo_ingresso == codigo:
                return inscricao
        return None
