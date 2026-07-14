"""Demonstração de persistência da Tarefa 1 — GestEventos.

Script narrado que SALVA e LÊ objetos das classes do modelo em arquivos JSON,
usando a camada de persistência. Ao final, os arquivos ficam na pasta ``data/``
para inspeção. Execute a partir da raiz do projeto:

    python exemplo_persistencia.py
"""
import sys
from datetime import date, datetime

# Garante a exibição correta de acentos no console do Windows.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from model.categoria import Categoria
from model.cupom_desconto import CupomDesconto
from model.evento import Evento
from model.local import Local
from model.lote_ingresso import LoteIngresso
from model.organizador import Organizador
from model.participante import Participante
from persistence.categoria_repositorio import CategoriaRepositorio
from persistence.cupom_desconto_repositorio import CupomDescontoRepositorio
from persistence.evento_repositorio import EventoRepositorio
from persistence.local_repositorio import LocalRepositorio
from persistence.lote_ingresso_repositorio import LoteIngressoRepositorio
from persistence.usuario_repositorio import UsuarioRepositorio


def separador(titulo: str) -> None:
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


def main() -> None:
    # Recomeça de um estado limpo para que a demonstração seja reproduzível.
    import os
    import shutil

    if os.path.isdir("data"):
        shutil.rmtree("data")

    # Repositórios (gravam em arquivos dentro de data/)
    repo_usuarios = UsuarioRepositorio()
    repo_categorias = CategoriaRepositorio()
    repo_locais = LocalRepositorio()
    repo_eventos = EventoRepositorio()
    repo_lotes = LoteIngressoRepositorio()
    repo_cupons = CupomDescontoRepositorio()

    # ---------------------------------------------------------------- #
    # 1) SALVAR objetos do modelo em arquivo
    # ---------------------------------------------------------------- #
    separador("1) SALVANDO objetos em arquivos JSON")

    organizador = repo_usuarios.inserir(
        Organizador(
            nome="Ana Souza",
            email="ana@ifrn.edu.br",
            login="ana",
            senha="123",
            instituicao="IFRN",
        )
    )
    participante = repo_usuarios.inserir(
        Participante(
            nome="Bruno Lima",
            email="bruno@email.com",
            login="bruno",
            senha="456",
            cpf="123.456.789-00",
            telefone="(84) 99999-0000",
        )
    )
    categoria = repo_categorias.inserir(Categoria("Tecnologia", "Eventos de TI e inovação"))
    local = repo_locais.inserir(
        Local("Auditório Central", "Av. Sen. Salgado Filho, 1559", "Natal", capacidade=300)
    )
    evento = repo_eventos.inserir(
        Evento(
            titulo="TechConf 2026",
            descricao="Conferência anual de tecnologia",
            data_hora=datetime(2026, 9, 15, 19, 30),
            organizador_id=organizador.id,
            categoria_id=categoria.id,
            local_id=local.id,
        )
    )
    repo_lotes.inserir(LoteIngresso("Lote 1", 80.0, 100, evento_id=evento.id))
    repo_lotes.inserir(LoteIngresso("VIP", 200.0, 20, evento_id=evento.id))
    repo_cupons.inserir(
        CupomDesconto("PROMO10", percentual_desconto=10.0, validade=date(2026, 12, 31))
    )

    print(f"Organizador salvo:  {organizador.nome} (id={organizador.id})")
    print(f"Participante salvo: {participante.nome} (id={participante.id})")
    print(f"Categoria salva:    {categoria}")
    print(f"Local salvo:        {local}")
    print(f"Evento salvo:       {evento}")

    # ---------------------------------------------------------------- #
    # 2) LER os objetos de volta a partir dos arquivos
    # ---------------------------------------------------------------- #
    separador("2) LENDO os objetos gravados nos arquivos JSON")

    print("Usuários (reconstruídos polimorficamente):")
    for usuario in repo_usuarios.listar_todos():
        print(f"  - {usuario.nome} | perfil={usuario.perfil()}")

    evento_lido = repo_eventos.buscar_por_id(evento.id)
    print(f"\nEvento lido: {evento_lido}")
    print(f"  data/hora recuperada: {evento_lido.data_hora}")

    print("\nLotes do evento (associação 1-para-muitos):")
    for lote in repo_lotes.listar_por_evento(evento.id):
        print(f"  - {lote}")

    # ---------------------------------------------------------------- #
    # 3) Demonstração de pesquisa e das primitivas de regra de negócio
    # ---------------------------------------------------------------- #
    separador("3) Pesquisa e regras de negócio (nível de modelo)")

    encontrados = repo_eventos.buscar_por_titulo("tech")
    print(f'Pesquisa por "tech": {[str(e) for e in encontrados]}')

    lote_vip = repo_lotes.listar_por_evento(evento.id)[1]
    cupom = repo_cupons.buscar_por_codigo("PROMO10")
    desconto = cupom.calcular_desconto(lote_vip.preco)
    print(
        f"\nLote {lote_vip.nome}: preço R$ {lote_vip.preco:.2f} | "
        f"cupom {cupom.codigo} válido? {cupom.esta_valido()} | "
        f"desconto R$ {desconto:.2f} | "
        f"valor final R$ {lote_vip.preco - desconto:.2f}"
    )
    print(f"Há disponibilidade no lote VIP? {lote_vip.ha_disponibilidade()}")

    separador("Arquivos gerados na pasta data/")
    print("usuarios.json, categorias.json, locais.json, eventos.json,")
    print("lotes_ingressos.json, cupons.json")


if __name__ == "__main__":
    main()
