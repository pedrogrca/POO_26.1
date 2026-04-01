class Viagem:
    def __init__(self):
        self.distancia = 0.0
        self.tempo = 0.0
    def set_distancia(self, d):
        self.distancia = d
    def set_tempo(self, t):
        self.tempo = t
    def get_distancia(self):
        return self.distancia
    def get_tempo(self):
        return self.tempo
    def velocidade_media(self):
        return self.distancia / (self.tempo / 60)
    
x = Viagem()

x.set_distancia(500)
x.set_tempo(200)

print(x.get_distancia())
print(x.get_tempo())

print(x.velocidade_media())