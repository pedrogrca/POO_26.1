class Cinema:
    def __init__(self, dia):
        self.dia = dia.lower()
        self.hora = 0
    def valor(self, dia, hora, valor_base, meia_entrada):
        if dia == 'quarta':
            return 8
        elif dia in ['segunda', 'terça', 'quinta']:
            valor_base = 16
            if hora >= 17 and hora <= 24:
                if meia_entrada:
                    return valor_base / 2
                else:
                    return valor_base * 1.50
            elif hora < 17:
                if meia_entrada:
                    return valor_base / 2
                else:
                    return valor_base
            else:
                return 'Seu horário é invalido'
        elif dia in ['sexta', 'sábado', 'domingo']:
            valor_base = 20
            if hora >= 17 and hora <= 24:
                if meia_entrada:
                    return valor_base / 2
                else:
                    return valor_base * 1.50
            elif hora < 17:
                if meia_entrada:
                    return valor_base / 2
                else:
                    return valor_base
            else:
                return 'Seu horário é invalido'

x = Cinema('segunda')
print(x.valor('segunda', 23, 0, True))