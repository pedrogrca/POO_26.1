import math

class Circulo:
    def __init__(self):
        self.raio = 0.0
    def set_raio(self,v):
        self.raio = v
    def get_raio(self):
        return self.raio
    def calc_area(self):
        return self.raio * math.pi ** 2
    def calc_circunferencia(self):
        return self.raio * math.pi * 2
    
x = Circulo()

x.set_raio(5)
valor_raio = x.raio

print(valor_raio)
print(x.calc_area())
print(x.calc_circunferencia())