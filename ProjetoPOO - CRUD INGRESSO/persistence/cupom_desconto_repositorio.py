"""Repositório de cupons de desconto."""
from model.cupom_desconto import CupomDesconto
from persistence.repositorio_json import RepositorioJson


class CupomDescontoRepositorio(RepositorioJson):
    def __init__(self, caminho_arquivo: str = "data/cupons.json"):
        super().__init__(caminho_arquivo, CupomDesconto)

    def buscar_por_codigo(self, codigo: str) -> CupomDesconto | None:
        """Localiza um cupom pelo código (usado ao aplicar desconto)."""
        termo = codigo.strip().upper()
        for cupom in self.listar_todos():
            if cupom.codigo.strip().upper() == termo:
                return cupom
        return None
