"""Testes da camada de serviço (operações e regras de negócio da Tarefa 2)."""
import os
import shutil
import tempfile
import unittest
from datetime import date, datetime

from model.inscricao import Inscricao
from persistence.categoria_repositorio import CategoriaRepositorio
from persistence.cupom_desconto_repositorio import CupomDescontoRepositorio
from persistence.evento_repositorio import EventoRepositorio
from persistence.inscricao_repositorio import InscricaoRepositorio
from persistence.local_repositorio import LocalRepositorio
from persistence.lote_ingresso_repositorio import LoteIngressoRepositorio
from persistence.pagamento_repositorio import PagamentoRepositorio
from persistence.usuario_repositorio import UsuarioRepositorio
from service.categoria_service import CategoriaService
from service.cupom_desconto_service import CupomDescontoService
from service.erros import ErroDeNegocio
from service.evento_service import EventoService
from service.inscricao_service import InscricaoService
from service.local_service import LocalService
from service.lote_ingresso_service import LoteIngressoService
from service.usuario_service import UsuarioService


class TestServico(unittest.TestCase):
    """Exercita os serviços usando repositórios em um diretório temporário."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()

        def caminho(nome):
            return os.path.join(self.dir, nome)

        usuarios = UsuarioRepositorio(caminho("usuarios.json"))
        categorias = CategoriaRepositorio(caminho("categorias.json"))
        locais = LocalRepositorio(caminho("locais.json"))
        eventos = EventoRepositorio(caminho("eventos.json"))
        lotes = LoteIngressoRepositorio(caminho("lotes.json"))
        cupons = CupomDescontoRepositorio(caminho("cupons.json"))
        inscricoes = InscricaoRepositorio(caminho("inscricoes.json"))
        pagamentos = PagamentoRepositorio(caminho("pagamentos.json"))

        self.usuario = UsuarioService(usuarios)
        self.categoria = CategoriaService(categorias)
        self.local = LocalService(locais)
        self.evento = EventoService(eventos, categorias, locais)
        self.lote = LoteIngressoService(lotes, eventos)
        self.cupom = CupomDescontoService(cupons)
        self.inscricao = InscricaoService(inscricoes, lotes, cupons, pagamentos)

        # Cenário base compartilhado pelos testes.
        self.org = self.usuario.cadastrar_organizador("Org", "o@x.com", "org", "1", "IFRN")
        self.participante = self.usuario.cadastrar_participante("Ana", "a@x.com", "ana", "1")
        categoria = self.categoria.inserir("Tecnologia")
        local = self.local.inserir("Auditório", "Rua A", "Natal", 100)
        self.evt = self.evento.inserir(
            "TechConf", "desc", datetime(2026, 9, 15, 19, 30),
            self.org.id, categoria.id, local.id,
        )
        self.lot = self.lote.inserir("Lote 1", 100.0, 2, self.evt.id)
        self.cup = self.cupom.inserir("PROMO10", 10.0, date(2027, 12, 31))

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    # ------------------------------------------------------------------ #
    def test_login_duplicado_e_autenticacao(self):
        with self.assertRaises(ErroDeNegocio):
            self.usuario.cadastrar_participante("Outra", "b@x.com", "ana", "9")
        self.assertEqual(self.usuario.autenticar("ana", "1").id, self.participante.id)
        with self.assertRaises(ErroDeNegocio):
            self.usuario.autenticar("ana", "senha_errada")

    def test_evento_exige_associacoes_validas(self):
        with self.assertRaises(ErroDeNegocio):
            self.evento.inserir("X", "", None, self.org.id, 999, 999)

    def test_realizar_inscricao_aplica_cupom_e_baixa_vaga(self):
        inscricao, pagamento = self.inscricao.realizar_inscricao(
            self.participante.id, self.lot.id, "PROMO10", "PIX"
        )
        # Cupom de 10% sobre R$100 -> R$90.
        self.assertEqual(inscricao.valor_final, 90.0)
        self.assertEqual(pagamento.valor, 90.0)
        # A vaga foi baixada no lote (2 -> 1).
        self.assertEqual(self.lote.buscar_por_id(self.lot.id).quantidade_disponivel, 1)

    def test_lote_esgotado_impede_inscricao(self):
        self.inscricao.realizar_inscricao(self.participante.id, self.lot.id)
        self.inscricao.realizar_inscricao(self.participante.id, self.lot.id)
        with self.assertRaises(ErroDeNegocio):  # vagas esgotadas (eram 2)
            self.inscricao.realizar_inscricao(self.participante.id, self.lot.id)

    def test_cancelar_devolve_vaga_e_estorna(self):
        inscricao, _ = self.inscricao.realizar_inscricao(self.participante.id, self.lot.id)
        self.inscricao.cancelar_inscricao(inscricao.id, self.participante.id)
        self.assertEqual(self.lote.buscar_por_id(self.lot.id).quantidade_disponivel, 2)
        pagamento = self.inscricao.buscar_pagamento(inscricao.id)
        self.assertEqual(pagamento.status, "ESTORNADO")

    def test_checkin_valida_uma_vez(self):
        inscricao, _ = self.inscricao.realizar_inscricao(self.participante.id, self.lot.id)
        validada = self.inscricao.validar_ingresso(inscricao.codigo_ingresso)
        self.assertTrue(validada.utilizado)
        with self.assertRaises(ErroDeNegocio):  # não pode validar duas vezes
            self.inscricao.validar_ingresso(inscricao.codigo_ingresso)

    def test_nao_cancela_ingresso_ja_utilizado(self):
        inscricao, _ = self.inscricao.realizar_inscricao(self.participante.id, self.lot.id)
        self.inscricao.validar_ingresso(inscricao.codigo_ingresso)
        with self.assertRaises(ErroDeNegocio):
            self.inscricao.cancelar_inscricao(inscricao.id, self.participante.id)


if __name__ == "__main__":
    unittest.main()
