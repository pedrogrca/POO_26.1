class ContaBancaria:
    def __init__(self, nome="", conta=0, saldo_inicial=0.0):
        self.__nome = nome
        self.__conta = conta
        self.__saldo = saldo_inicial

    def setNome(self, nome):
        self.__nome = nome
    def setConta(self, conta):
        self.__conta = conta
    def getNome(self):
        return self.__nome
    def getConta(self):
        return self.__conta
    def getSaldo(self):
        return self.__saldo
    
    def deposito(self, valor):
        if valor <= 0:
            return "Seu depósito precisa ser maior que 0"
        self.__saldo += valor
        return f"Olá {self.__nome}, seu depósito de R${valor} realizado. Novo saldo: R${self.__saldo}"

    def saque(self, valor):
        if valor > self.__saldo:
            return "Saldo insuficiente"
        if valor <= 0:
            return "Valor de saque inválido"
        self.__saldo -= valor
        return f"Olá {self.__nome}, seu saque de R${valor} realizado. Novo saldo: R${self.__saldo}"

class CaixaEletronico:
    def __init__(self, conta_objeto):
        self.conta = conta_objeto

    def iniciar(self):
        while True:
            y = input("Operação: (Saque / Deposito / Saldo / Sair): ").lower().strip()
            
            if y == "deposito":
                valor = float(input("Digite o valor do depósito: R$"))
                print(self.conta.deposito(valor))
            elif y == "saque":
                valor = float(input(f"Saldo atual: R${self.conta.getSaldo()}. Digite o valor do saque: R$"))
                print(self.conta.saque(valor))
            elif y == "saldo":
                print(f"Seu saldo atual é de R${self.conta.getSaldo()}")
            elif y == "sair":
                print("Au revoir!")
                break
            else:
                print("Opção inválida!")

x = ContaBancaria("Pedro", 1000, 5000.0)

menu = CaixaEletronico(x)
menu.iniciar()