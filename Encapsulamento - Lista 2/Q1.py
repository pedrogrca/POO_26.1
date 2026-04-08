import math

class Circulo:
    def __init__(self):
        self.__raio = 0.0
    def set_raio(self,v):
        if v <= 0:
            return "O valor do raio precisa ser maior que 0"
        else:
            self.__raio = v
    def get_raio(self):
        return self.__raio
    def calc_area(self):
        return  math.pi * (self.__raio  ** 2)
    def calc_circunferencia(self):
        return self.__raio * math.pi * 2
    
x = Circulo()

valor_digitado = int(input("Digite o valor do raio: "))

mensagem = x.set_raio(valor_digitado)

if mensagem: 
    print(mensagem)
else:
    print("Área:", x.calc_area())
    print("Circunferência:", x.calc_circunferencia())