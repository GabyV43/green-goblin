lista = [1, -1, 1, 1, -1]

"""
P B P P B
 B B P B
  P B B
   B P
    B
"""

# converter ele
nova_lista = []
for val in lista:
    nova_lista.append(val == -1)

# True => Branco
# False => Preto

resultado = False
for val in nova_lista:
    resultado ^= val

if resultado:
    print("Branco")
else:
    print("Preto")
