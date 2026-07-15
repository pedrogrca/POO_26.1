"""Exceção de regra de negócio."""


class ErroDeNegocio(Exception):
    """Erro previsível de regra de negócio.

    É lançado pelos serviços quando uma operação viola uma regra do sistema
    (ex.: login duplicado, lote esgotado, cupom inválido) e é tratado pela
    camada de interface (``view``), que apresenta a mensagem ao usuário.
    """
