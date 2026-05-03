class Cliente:
    def __init__(self, id, n, e, f):
        self.setId(id)
        self.setNome(n)
        self.setEmail(e)
        self.setFone(f)

    def ToString(self):
        return f'Cliente N°{self.__id}, Nome: {self.__nome}, E-mail: {self.__email}, Telefone: {self.__fone}'
    
    def setId(self, id):
        if id > 0:
            self.__id = id
        else: raise ValueError("Seu ID é Invalido!")

    def setNome(self, n):
        if n != "":
            self.__nome = n
        else: raise ValueError("Seu Nome está vazio!")

    def setEmail(self, e):
        if e != "":
            self.__email = e
        else: raise ValueError("Seu Email está vazio!")

    def setFone(self, f):
        if f != "":
            self.__fone = f
        else: raise ValueError("Seu Telefone está vazio!")

    def getID(self):
        return self.__id
    
    def getNome(self):
        return self.__nome
    
    def getEmail(self):
        return self.__email
    
    def getFone(self):
        return self.__fone
    

x = Cliente(1000, "Pedro", "pedro@gmail.com", "telefonefd")

print(x.ToString())