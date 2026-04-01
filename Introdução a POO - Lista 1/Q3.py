class ContaBancaria:
    def __init__(self, nome, conta, saldo):
        self.nome = nome
        self.conta = conta
        self.saldo = saldo
    def deposito(self,valor):
        if valor < 0:
            return "Seu depósito precisa ser maior que 0"
        else:
            self.saldo += valor
            return f"Olá {self.nome}, seu depósito de R${valor} foi concluido com sucesso, seu novo saldo é R${self.saldo} para a conta número {self.conta}"
    def saque (self,valor):
        if valor > self.saldo:
            return "Saldo insuficiente"
        else:
            self.saldo -= valor
            return f"Olá {self.nome}, seu saque de R${valor} foi concluido com sucesso, seu novo saldo é R${self.saldo} para a conta número {self.conta}"
        

x = ContaBancaria("Pedro", 1000, 5000)


print(x.deposito(500))
print(x.saque(200))