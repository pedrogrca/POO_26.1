import math

class Circulo:
    def __init__(self):
        self.raio = 0
    def calc_area(self):
        return self.raio * math.pi ** 2
    def calc_circ(self):
        return 2 * self.raio * math.pi
    
x = Circulo()

x.raio = 5

print(x.calc_area())
print(x.calc_circ())