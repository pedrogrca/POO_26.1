class Frete():
    def __init__(self,p = 0.0,d = 0.0):
        self.__peso = p
        self.__distancia = d
    def setDistancia(self,d):
        if d > 1:
            self.__distancia = d
        else: raise ValueError("Digite um valor válido")
    def setPeso(self,p):
        if p > 0:
            self.__peso = p
        else: raise ValueError("Digite um valor válido")
    def getDistancia(self):
        return self.__distancia
    def getPeso(self):
        return self.__peso
    def calcFrete(self):
        return (self.__peso * self.__distancia) * 0.01
    def toString(self):
        return f"O frete para seu pedido de {self.getPeso()}kg para a distância de {self.getDistancia()}km custará um total de R${self.calcFrete()}"
    

x = Frete()

x.setPeso(100)
x.setDistancia(50)

print(x.toString())