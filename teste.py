# n = altura
# m = largura

n_linhas, n_colunas = map(int, input().split())

matrizA = []

for i in range(n_linhas):
    linha = list(map(int, input().split()))
    matrizA.append(linha)

# matrizB = []

# for i in range(n):
#     linha = list(map(int, input().split()))
#     matrizB.append(linha)


# # soma de matrizes
# resultado = []
# for i in range(n):
#     linha = []
#     for j in range(m):
#         linha.append(matrizA[i][j] + matrizB[i][j])
#     resultado.append(linha)

# print(resultado)


# produto
# x, y = map(int, input().split())

# matrizC = []

# for i in range(n):
#     linha = list(map(int, input().split()))
#     matrizC.append(linha)

# # pode fazer o produto?

# # quero fazer A * C

# if m != x:
#     raise Exception("não dá")

# a, b = n, y

# resultado = []

# for i in range(a):
#     linha = []
#     for j in range(b):
#         valor = 0
#         for k in range(m):
#             valor += matrizA[i][k] * matrizC[k][j]
#         linha.append(valor)
#     resultado.append(linha)

# print(resultado)

# soma debaixo da diagonal

if n_linhas == n_colunas:
    soma = 0
    for i in range(n_linhas):
        for j in range(n_colunas):
            if i > j:
                soma += matrizA[i][j]

    soma2 = 0
    for j in range(n_colunas):
        for i in range(j+1, n_linhas):
            soma2 += matrizA[i][j]
