"""Funções de formatação para apresentação de objetos na interface."""


def descrever_evento(servicos, evento) -> str:
    """Monta uma linha descritiva de um evento com categoria e local."""
    categoria = servicos.categoria.buscar_por_id(evento.categoria_id)
    local = servicos.local.buscar_por_id(evento.local_id)
    return (
        f"{evento} | Categoria: {categoria.nome if categoria else '-'}"
        f" | Local: {local.nome if local else '-'}"
    )
