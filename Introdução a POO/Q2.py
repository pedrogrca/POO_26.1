class Viagem:
    def __init__(self):
        self.distancia = 0
        self.tempo = 0
    def velocidade_media(self):
        return self.distancia / (self.tempo / 60)
    
x = Viagem()

x.distancia = 500
x.tempo = 200

print(x.velocidade_media())
