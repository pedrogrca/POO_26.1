"""Repositório de pagamentos."""
from model.pagamento import Pagamento
from persistence.repositorio_json import RepositorioJson


class PagamentoRepositorio(RepositorioJson):
    def __init__(self, caminho_arquivo: str = "data/pagamentos.json"):
        super().__init__(caminho_arquivo, Pagamento)

    def buscar_por_inscricao(self, inscricao_id: int) -> Pagamento | None:
        """Associação um-para-um: retorna o pagamento de uma inscrição."""
        for pagamento in self.listar_todos():
            if pagamento.inscricao_id == inscricao_id:
                return pagamento
        return None
