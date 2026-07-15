"""Ponto de entrada do GestEventos.

Arquitetura em camadas:
    model        -> entidades de negócio
    persistence  -> repositórios (CRUD em arquivos JSON)
    service      -> operações e regras de negócio
    view         -> interface com o usuário (menus por perfil)

Execute com:  python main.py
"""
import sys

from service.servicos import Servicos
from view.tela_login import TelaLogin

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    servicos = Servicos()
    try:
        TelaLogin(servicos).executar()
    except (KeyboardInterrupt, EOFError):
        print("\nSistema encerrado.")


if __name__ == "__main__":
    main()
