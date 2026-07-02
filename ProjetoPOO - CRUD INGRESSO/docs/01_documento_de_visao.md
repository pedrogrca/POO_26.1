# Documento de Visão do Sistema

**Disciplina:** Programação Orientada a Objetos — 2º Bimestre — 2026.1
**Curso:** Tecnologia em Análise e Desenvolvimento de Sistemas — IFRN / DIATINF
**Tarefa:** Tarefa 1 — Documento de Visão

---

## 1. Título do Projeto

**GestEventos — Sistema de Gestão de Eventos e Ingressos**

## 2. Objetivo do Sistema

O GestEventos tem por objetivo apoiar a **organização, divulgação e comercialização de
ingressos para eventos e conferências**. O sistema permite que **organizadores**
cadastrem eventos, definam lotes de ingressos (com preços e quantidades distintas) e
criem cupons de desconto, enquanto **participantes** pesquisam eventos, inscrevem-se e
geram seus ingressos, com aplicação automática de descontos e controle de vagas.

## 3. Descrição do Problema a Ser Resolvido

A venda de ingressos para eventos envolve regras que, quando controladas manualmente
(planilhas, mensagens, anotações), geram erros frequentes:

- **Controle de vagas:** vender mais ingressos do que a capacidade de um lote (overbooking).
- **Preços por lote:** um mesmo evento costuma ter faixas de preço distintas (Lote 1,
  Lote 2, VIP), cada uma com quantidade própria e esgotamento independente.
- **Descontos:** aplicação de cupons promocionais de forma consistente e dentro da validade.
- **Cálculo do valor final:** o valor pago deve considerar o preço do lote menos o desconto.
- **Rastreabilidade:** relacionar cada ingresso ao participante, ao lote, ao evento e ao
  respectivo pagamento, permitindo validação (check-in) e eventual cancelamento.

O GestEventos centraliza essas informações e **automatiza a regra de negócio central**:
ao efetivar uma inscrição, o sistema verifica a disponibilidade no lote, decrementa a
quantidade disponível, gera o ingresso, aplica o cupom de desconto (se houver), calcula
o valor final e registra o pagamento — tudo em uma única operação transacional.

## 4. Perfis de Usuários Envolvidos

| Perfil | Descrição | Responsabilidades |
|--------|-----------|-------------------|
| **Organizador** | Usuário responsável por criar e administrar eventos. | Cadastra categorias, locais, eventos, lotes de ingressos e cupons; valida ingressos (check-in); acompanha inscrições. |
| **Participante** | Usuário que consome os eventos. | Cadastra-se, pesquisa eventos, realiza inscrições (compra de ingressos), aplica cupons, consulta e cancela seus ingressos. |

O acesso ao sistema é controlado por **login e senha**, e o **menu de operações é exibido
de acordo com o perfil** do usuário autenticado.

## 5. Entidades do Sistema

**Controle de usuários**

- `Usuario` (classe base) → especializações `Organizador` e `Participante`.

**Entidades de negócio**

1. `Categoria` — classifica os eventos (ex.: Tecnologia, Música, Educação).
2. `Local` — onde o evento acontece (endereço, cidade, capacidade).
3. `Evento` — o evento/conferência propriamente dito.
4. `LoteIngresso` — faixa de ingressos de um evento (ex.: Lote 1, Lote 2, VIP).
5. `CupomDesconto` — cupom promocional aplicável a uma inscrição (opcional).
6. `Inscricao` (Venda) — registro da compra/geração de um ingresso.
7. `Pagamento` — pagamento associado a uma inscrição.

**Relacionamentos de associação (um-para-muitos)**

- Um `Organizador` cria muitos `Evento`.
- Uma `Categoria` classifica muitos `Evento`.
- Um `Local` sedia muitos `Evento`.
- Um `Evento` possui muitos `LoteIngresso`.
- Um `Participante` realiza muitas `Inscricao`.
- Um `LoteIngresso` gera muitas `Inscricao`.
- Um `CupomDesconto` pode ser usado em muitas `Inscricao` (opcional).
- Uma `Inscricao` possui um `Pagamento`.

## 6. Lista de Operações do Aplicativo

### 6.1. Operações comuns (autenticação)

- **Entrar no sistema** (login com validação de perfil).
- **Sair do sistema** (logout).
- **Cadastrar-se** como participante.

### 6.2. Operações do Organizador

**CRUD das entidades**

- Categoria: inserir, listar, atualizar, excluir.
- Local: inserir, listar, atualizar, excluir.
- Evento: inserir, listar, atualizar, excluir.
- LoteIngresso: inserir, listar, atualizar, excluir.
- CupomDesconto: inserir, listar, atualizar, excluir.

**Associação entre objetos**

- Vincular um `Evento` a uma `Categoria`, a um `Local` e ao `Organizador` que o criou.
- Vincular um `LoteIngresso` a um `Evento`.

**Pesquisa (listagem parcial)**

- Pesquisar eventos por parte do título.
- Listar eventos por categoria.
- Listar as inscrições/ingressos de um evento.

**Regras de negócio**

- **Validar ingresso (check-in):** localiza a inscrição pelo código do ingresso e a marca
  como *utilizada*, impedindo reutilização.

### 6.3. Operações do Participante

**Pesquisa (listagem parcial)**

- Pesquisar eventos por parte do título.
- Listar eventos por categoria.
- Visualizar os lotes de ingressos disponíveis de um evento.

**Regras de negócio (manipulam mais de uma entidade)**

- **Realizar inscrição (comprar ingresso):** verifica a disponibilidade no `LoteIngresso`;
  havendo vaga, decrementa a quantidade disponível, aplica o `CupomDesconto` (se informado
  e válido), calcula o valor final, cria a `Inscricao` com um código de ingresso único e
  registra o `Pagamento` correspondente.
- **Cancelar inscrição:** marca a `Inscricao` como *cancelada*, devolve a vaga ao
  `LoteIngresso` (incrementa a quantidade disponível) e estorna o `Pagamento`.

**Consultas**

- Listar minhas inscrições/ingressos.
- Consultar detalhes de um ingresso.

---

> **Observação sobre a arquitetura:** o sistema é organizado em camadas — **model**
> (entidades de negócio), **persistência** (repositórios que gravam/leem objetos em
> arquivos JSON) e, nas etapas seguintes, **view/service** (operações) e **template**
> (interface com o usuário). Esta Tarefa 1 entrega o **model** e a **persistência**.
