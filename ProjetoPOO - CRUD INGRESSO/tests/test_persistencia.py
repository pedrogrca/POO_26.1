"""Códigos de teste da Tarefa 1.

Demonstram, de forma automatizada, o requisito exigido no PDF:
"salvar e ler um objeto de uma classe do modelo em arquivo".

Cada teste grava objetos do modelo em arquivos JSON (usando os repositórios da
camada de persistência) e, em seguida, os lê de volta, verificando se os dados
foram preservados. Também são exercitados o CRUD completo, as pesquisas, as
associações e os métodos das regras de negócio.

Execução:
    python -m unittest tests.test_persistencia      (a partir da raiz do projeto)
    python tests/test_persistencia.py
"""
import os
import sys
import tempfile
import unittest
from datetime import date, datetime

# Permite executar o arquivo diretamente (adiciona a raiz do projeto ao path).
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.categoria import Categoria
from model.cupom_desconto import CupomDesconto
from model.evento import Evento
from model.inscricao import Inscricao
from model.local import Local
from model.lote_ingresso import LoteIngresso
from model.organizador import Organizador
from model.pagamento import Pagamento
from model.participante import Participante
from persistence.categoria_repositorio import CategoriaRepositorio
from persistence.cupom_desconto_repositorio import CupomDescontoRepositorio
from persistence.evento_repositorio import EventoRepositorio
from persistence.inscricao_repositorio import InscricaoRepositorio
from persistence.lote_ingresso_repositorio import LoteIngressoRepositorio
from persistence.pagamento_repositorio import PagamentoRepositorio
from persistence.usuario_repositorio import UsuarioRepositorio


class TestPersistencia(unittest.TestCase):
    """Testes de salvar/ler objetos do modelo em arquivo JSON."""

    def setUp(self):
        # Diretório temporário isolado para não afetar os dados reais.
        self._dir = tempfile.TemporaryDirectory()
        self.base = self._dir.name

    def tearDown(self):
        self._dir.cleanup()

    def caminho(self, arquivo: str) -> str:
        return os.path.join(self.base, arquivo)

    # ------------------------------------------------------------------ #
    # Requisito principal: salvar e ler um objeto do modelo em arquivo
    # ------------------------------------------------------------------ #
    def test_salvar_e_ler_categoria(self):
        repo = CategoriaRepositorio(self.caminho("categorias.json"))

        # Salvar
        salva = repo.inserir(Categoria(nome="Tecnologia", descricao="Eventos de TI"))
        self.assertEqual(salva.id, 1)  # id atribuído automaticamente
        self.assertTrue(os.path.exists(self.caminho("categorias.json")))

        # Ler de volta
        lida = repo.buscar_por_id(1)
        self.assertIsNotNone(lida)
        self.assertIsInstance(lida, Categoria)
        self.assertEqual(lida.nome, "Tecnologia")
        self.assertEqual(lida.descricao, "Eventos de TI")

    def test_salvar_e_ler_evento_com_datetime(self):
        repo = EventoRepositorio(self.caminho("eventos.json"))
        data = datetime(2026, 9, 15, 19, 30)

        repo.inserir(
            Evento(
                titulo="TechConf 2026",
                descricao="Conferência de tecnologia",
                data_hora=data,
                organizador_id=1,
                categoria_id=2,
                local_id=3,
            )
        )

        lido = repo.buscar_por_id(1)
        self.assertEqual(lido.titulo, "TechConf 2026")
        self.assertEqual(lido.data_hora, data)  # datetime preservado
        self.assertEqual(lido.organizador_id, 1)
        self.assertEqual(lido.categoria_id, 2)
        self.assertEqual(lido.local_id, 3)

    def test_salvar_e_ler_cupom_com_date(self):
        repo = CupomDescontoRepositorio(self.caminho("cupons.json"))
        repo.inserir(
            CupomDesconto(codigo="PROMO10", percentual_desconto=10.0, validade=date(2026, 12, 31))
        )

        lido = repo.buscar_por_id(1)
        self.assertEqual(lido.codigo, "PROMO10")
        self.assertEqual(lido.validade, date(2026, 12, 31))
        self.assertAlmostEqual(lido.calcular_desconto(200.0), 20.0)

    # ------------------------------------------------------------------ #
    # Polimorfismo: um único repositório grava/lê subtipos de Usuario
    # ------------------------------------------------------------------ #
    def test_salvar_e_ler_usuarios_polimorficos(self):
        repo = UsuarioRepositorio(self.caminho("usuarios.json"))
        repo.inserir(
            Organizador(nome="Ana", email="ana@ifrn.edu.br", login="ana", senha="123", instituicao="IFRN")
        )
        repo.inserir(
            Participante(nome="Bruno", email="bruno@x.com", login="bruno", senha="456", cpf="111", telefone="9999")
        )

        usuarios = repo.listar_todos()
        self.assertEqual(len(usuarios), 2)
        self.assertIsInstance(usuarios[0], Organizador)
        self.assertIsInstance(usuarios[1], Participante)
        self.assertEqual(usuarios[0].perfil(), "ORGANIZADOR")
        self.assertEqual(usuarios[1].perfil(), "PARTICIPANTE")

        # Consulta específica do repositório (usada na autenticação)
        encontrado = repo.buscar_por_login("bruno")
        self.assertIsInstance(encontrado, Participante)
        self.assertTrue(encontrado.verificar_senha("456"))
        self.assertFalse(encontrado.verificar_senha("errada"))

    # ------------------------------------------------------------------ #
    # CRUD completo: inserir, listar, atualizar e excluir
    # ------------------------------------------------------------------ #
    def test_crud_completo(self):
        from persistence.local_repositorio import LocalRepositorio

        repo = LocalRepositorio(self.caminho("locais.json"))

        # inserir
        repo.inserir(Local(nome="Auditório A", cidade="Natal", capacidade=200))
        repo.inserir(Local(nome="Auditório B", cidade="Mossoró", capacidade=100))
        self.assertEqual(len(repo.listar_todos()), 2)

        # atualizar
        local = repo.buscar_por_id(1)
        local.capacidade = 250
        self.assertTrue(repo.atualizar(local))
        self.assertEqual(repo.buscar_por_id(1).capacidade, 250)

        # excluir
        self.assertTrue(repo.excluir(2))
        self.assertFalse(repo.excluir(2))  # já não existe
        self.assertEqual(len(repo.listar_todos()), 1)

    # ------------------------------------------------------------------ #
    # Pesquisas e associações
    # ------------------------------------------------------------------ #
    def test_pesquisa_parcial_por_titulo(self):
        repo = EventoRepositorio(self.caminho("eventos.json"))
        repo.inserir(Evento(titulo="TechConf 2026", categoria_id=1))
        repo.inserir(Evento(titulo="Festival de Música", categoria_id=2))
        repo.inserir(Evento(titulo="Tech Meetup", categoria_id=1))

        resultado = repo.buscar_por_titulo("tech")
        self.assertEqual(len(resultado), 2)

        por_categoria = repo.listar_por_categoria(1)
        self.assertEqual(len(por_categoria), 2)

    def test_associacao_lotes_por_evento(self):
        repo = LoteIngressoRepositorio(self.caminho("lotes.json"))
        repo.inserir(LoteIngresso(nome="Lote 1", preco=50.0, quantidade_total=100, evento_id=1))
        repo.inserir(LoteIngresso(nome="VIP", preco=150.0, quantidade_total=20, evento_id=1))
        repo.inserir(LoteIngresso(nome="Lote 1", preco=30.0, quantidade_total=50, evento_id=2))

        lotes_evento_1 = repo.listar_por_evento(1)
        self.assertEqual(len(lotes_evento_1), 2)

    # ------------------------------------------------------------------ #
    # Métodos das regras de negócio (nível de modelo)
    # ------------------------------------------------------------------ #
    def test_regras_do_lote(self):
        lote = LoteIngresso(nome="VIP", preco=100.0, quantidade_total=2)
        self.assertTrue(lote.ha_disponibilidade())
        lote.decrementar()
        lote.decrementar()
        self.assertFalse(lote.ha_disponibilidade())
        with self.assertRaises(ValueError):
            lote.decrementar()  # esgotado
        lote.incrementar()
        self.assertEqual(lote.quantidade_disponivel, 1)

    def test_inscricao_e_pagamento_roundtrip(self):
        repo_insc = InscricaoRepositorio(self.caminho("inscricoes.json"))
        repo_pag = PagamentoRepositorio(self.caminho("pagamentos.json"))

        inscricao = repo_insc.inserir(
            Inscricao(
                codigo_ingresso="ABC123",
                participante_id=1,
                lote_id=1,
                valor_original=100.0,
                valor_final=90.0,
                cupom_id=1,
            )
        )
        repo_pag.inserir(Pagamento(inscricao_id=inscricao.id, valor=90.0, forma_pagamento="PIX"))

        lida = repo_insc.buscar_por_codigo_ingresso("ABC123")
        self.assertEqual(lida.valor_final, 90.0)
        self.assertEqual(lida.status, Inscricao.STATUS_CONFIRMADA)

        pagamento = repo_pag.buscar_por_inscricao(inscricao.id)
        self.assertIsNotNone(pagamento)
        self.assertEqual(pagamento.valor, 90.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
