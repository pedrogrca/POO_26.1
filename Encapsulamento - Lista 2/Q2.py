class Viagem:
    def __init__(self):
        self.__distancia = 0.0
        self.__tempo = 0.0
    def set_distancia(self, d):
        if d <= 0:
            print("Erro: A distância precisa ser maior que 0.")
            return False
        else:
            self.__distancia = d 
            return True
            
    def set_tempo(self, t):
        if t <= 0:
            print("❌ Erro: O tempo precisa ser maior que 0.")
            return False
        else: 
            self.__tempo = t
            return True

    def get_distancia(self):
        return self.__distancia
    def get_tempo(self):
        return self.__tempo
    def velocidade_media(self):
        return self.__distancia / (self.__tempo / 60)

x = Viagem()

while True:
    d = float(input("Digite o valor da distância (em KM): "))
    valid = x.set_distancia(d)
    if valid == True:
        break

while True:
    t = float(input("Digite o valor do tempo (em minutos): "))
    valid = x.set_tempo(t)
    if valid == True:
        break

print(f"A velocidade média é: {x.velocidade_media():.2f} km/h")