# GestEventos — Sistema de Gestão de Eventos e Ingressos

Projeto da disciplina de **Programação Orientada a Objetos** (2º Bimestre — 2026.1),
Tecnologia em Análise e Desenvolvimento de Sistemas — IFRN/DIATINF.

> **Escopo desta entrega: Tarefa 1 (40 pontos).**
> Tema livre (não é comércio eletrônico): gestão de eventos, lotes de ingressos,
> inscrições/vendas e cupons de desconto. Projeto **em dupla** (7 entidades de negócio
> + controle de usuários), **persistência em arquivos JSON**, feito em **Python**.

---

## Entregáveis da Tarefa 1

| Item | Pontos | Arquivo(s) |
|------|:------:|------------|
| Documento de Visão do Sistema | 5 | [docs/01_documento_de_visao.md](docs/01_documento_de_visao.md) |
| Diagrama de Casos de Uso | 5 | [docs/02_diagrama_casos_de_uso.puml](docs/02_diagrama_casos_de_uso.puml) · [PNG](docs/img/diagrama_casos_de_uso.png) |
| Diagrama de Classes do Modelo | 10 | [docs/03_diagrama_classes_modelo.puml](docs/03_diagrama_classes_modelo.puml) · [PNG](docs/img/diagrama_classes_modelo.png) |
| Diagrama de Classes da Persistência | (10) | [docs/04_diagrama_classes_persistencia.puml](docs/04_diagrama_classes_persistencia.puml) · [PNG](docs/img/diagrama_classes_persistencia.png) |
| Implementação Modelo + Persistência | 20 | pastas [`model/`](model) e [`persistence/`](persistence) |
| Código de teste (salvar/ler em arquivo) | (20) | [tests/test_persistencia.py](tests/test_persistencia.py) · [exemplo_persistencia.py](exemplo_persistencia.py) |

## Arquitetura em camadas

```
ProjetoPOO/
├── model/            # Camada de MODELO (entidades de negócio)
│   ├── entidade_base.py      # superclasse abstrata (id + to_dict/from_dict)
│   ├── usuario.py            # base abstrata dos usuários (fábrica polimórfica)
│   ├── organizador.py        # perfil Organizador
│   ├── participante.py       # perfil Participante
│   ├── categoria.py
│   ├── local.py
│   ├── evento.py
│   ├── lote_ingresso.py
│   ├── cupom_desconto.py
│   ├── inscricao.py
│   └── pagamento.py
├── persistence/      # Camada de PERSISTÊNCIA (repositórios JSON)
│   ├── repositorio_json.py   # CRUD genérico em arquivo JSON
│   └── *_repositorio.py      # um repositório por entidade + consultas
├── tests/
│   └── test_persistencia.py  # testes automatizados de salvar/ler
├── exemplo_persistencia.py   # demonstração narrada (salva e lê objetos)
├── data/                     # arquivos .json gerados em tempo de execução
└── docs/                     # documento de visão e diagramas
```

As camadas **view/service** (operações) e **template** (interface com o usuário)
serão implementadas na **Tarefa 2**.

## Entidades e relacionamentos (associação um-para-muitos)

- Um **Organizador** cria muitos **Eventos**.
- Uma **Categoria** classifica muitos **Eventos**.
- Um **Local** sedia muitos **Eventos**.
- Um **Evento** possui muitos **LotesIngresso** (ex.: Lote 1, Lote 2, VIP).
- Um **Participante** realiza muitas **Inscrições**.
- Um **LoteIngresso** origina muitas **Inscrições**.
- Um **CupomDesconto** pode ser aplicado em muitas **Inscrições** (opcional).
- Uma **Inscrição** gera um **Pagamento**.

## Como executar

Requer **Python 3.10+** (usa `tipo | None`). Não há dependências externas — apenas a
biblioteca padrão. Execute a partir da **raiz do projeto**:

```bash
# Testes automatizados (salvar e ler objetos do modelo em arquivo)
python -m unittest tests.test_persistencia -v

# Demonstração narrada (gera os arquivos JSON em data/)
python exemplo_persistencia.py
```

## Como visualizar/renderizar os diagramas

Os diagramas já estão renderizados em [`docs/img/`](docs/img). Para regenerá-los a
partir do código-fonte `.puml`, use a extensão **PlantUML** do VS Code ou o site
<https://www.plantuml.com/plantuml>. Via linha de comando (com o `plantuml.jar`):

```bash
java -jar plantuml.jar -charset UTF-8 -tpng -o img docs/*.puml
```
