"""Camada de serviço (operações/regras de negócio) do GestEventos.

Os serviços orquestram os repositórios da camada de persistência e
implementam as regras de negócio do sistema. Não realizam entrada/saída de
dados com o usuário (isso é responsabilidade da camada ``view``): quando uma
regra é violada, lançam :class:`~service.erros.ErroDeNegocio`.
"""
