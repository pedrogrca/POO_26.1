# Qgit 1

soma_par = 0
soma_impar = 0

for i in range(4):
    n = int(input())

    if n % 2 == 0:
        soma_par += n

    else:
        soma_impar += n

print(f'Soma dos pares: {soma_par}')
print(f'Soma dos impares: {soma_impar}')