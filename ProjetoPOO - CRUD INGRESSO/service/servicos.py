"""Contêiner de serviços: cria os repositórios e injeta-os nos serviços.

Centraliza a composição das camadas de persistência e serviço, de modo que a
camada de interface (``view``) receba apenas um objeto ``Servicos`` e não
precise conhecer os repositórios diretamente.
"""
from datetime import date, datetime

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
from persistence.inscricao_repositorio import InscricaoRepositorio
from persistence.local_repositorio import LocalRepositorio
from persistence.lote_ingresso_repositorio import LoteIngressoRepositorio
from persistence.pagamento_repositorio import PagamentoRepositorio
from persistence.usuario_repositorio import UsuarioRepositorio
from service.categoria_service import CategoriaService
from service.cupom_desconto_service import CupomDescontoService
from service.evento_service import EventoService
from service.inscricao_service import InscricaoService
from service.local_service import LocalService
from service.lote_ingresso_service import LoteIngressoService
from service.usuario_service import UsuarioService


class Servicos:
    """Fachada que expõe os serviços já configurados do sistema."""

    def __init__(self):
        # ------- Camada de persistência (repositórios) -------
        self._usuarios = UsuarioRepositorio()
        self._categorias = CategoriaRepositorio()
        self._locais = LocalRepositorio()
        self._eventos = EventoRepositorio()
        self._lotes = LoteIngressoRepositorio()
        self._cupons = CupomDescontoRepositorio()
        self._inscricoes = InscricaoRepositorio()
        self._pagamentos = PagamentoRepositorio()

        # ------- Camada de serviço (operações) -------
        self.usuario = UsuarioService(self._usuarios)
        self.categoria = CategoriaService(self._categorias)
        self.local = LocalService(self._locais)
        self.evento = EventoService(self._eventos, self._categorias, self._locais)
        self.lote = LoteIngressoService(self._lotes, self._eventos)
        self.cupom = CupomDescontoService(self._cupons)
        self.inscricao = InscricaoService(
            self._inscricoes, self._lotes, self._cupons, self._pagamentos
        )

    def carregar_demo(self) -> bool:
        """Cria dados de demonstração se ainda não existirem. Retorna ``True``
        quando os dados foram criados nesta chamada."""
        if self._usuarios.buscar_por_login("admin") is not None:
            return False
        org = self._usuarios.inserir(
            Organizador("Administrador", "admin@gesteventos.com", "admin", "admin", "IFRN")
        )
        self._usuarios.inserir(
            Participante("Maria Silva", "maria@email.com", "maria", "123",
                         "000.000.000-00", "99999-0000")
        )
        categoria = self._categorias.inserir(Categoria("Tecnologia", "Eventos de tecnologia"))
        local = self._locais.inserir(Local("Auditório Central", "Av. Salgado Filho", "Natal", 300))
        evento = self._eventos.inserir(
            Evento("TechConf 2026", "Conferência de tecnologia",
                   datetime(2026, 9, 15, 19, 30), org.id, categoria.id, local.id)
        )
        self._lotes.inserir(LoteIngresso("Lote 1", 80.0, 100, evento_id=evento.id))
        self._lotes.inserir(LoteIngresso("VIP", 200.0, 20, evento_id=evento.id))
        self._cupons.inserir(CupomDesconto("PROMO10", 10.0, validade=date(2027, 12, 31)))
        return True
