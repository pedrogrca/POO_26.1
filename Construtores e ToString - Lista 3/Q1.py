class Retangulo:
    def __init__(self):
        self.__base = 0.0
        self.__altura = 0.0
    def setBase(self, b):
        if b > 0:
            self.__base = b
        else: raise ValueError()
    def setAltura(self, a):
        if a > 0:
            self.__altura = a
        else: raise ValueError()
    def getBase(self):
        return self.__base
    def getAltura (self):
        return self.__altura
    def calcArea(self):
        return self.__base * self.__altura
    def calcDiagonal(self):
        return (self.__altura ** 2) + (self.__base ** 2)
    def ToString(self):
        return f"A base eh {self.getBase()} e a altura eh {self.getAltura()}"
    

x = Retangulo()

x.setBase(10)
x.setAltura(5)

print(x.calcArea())
print(x.calcDiagonal())

print(x.ToString())