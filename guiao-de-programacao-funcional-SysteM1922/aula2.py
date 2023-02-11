#Exercicio 4.1
impar = None

#Exercicio 4.2
positivo = None

#Exercicio 4.3
comparar_modulo = None

#Exercicio 4.4
cart2pol = None

#Exercicio 4.5
ex5 = None

#Exercicio 4.6
def quantificador_universal(lista, f):
    if len(lista) != 0:
        if not f(lista[-1]):
            return False
        return quantificador_universal(lista[:-2], f)
    return True

#Exercicio 4.8
def subconjunto(lista1, lista2):
    if len(lista1) != 0:
        if lista1[0] not in lista2:
            return False
        return subconjunto(lista1[1:], lista2)
    return True

#Exercicio 4.9
def ordem(lista, f):
    if len(lista) > 1:
        if f(lista[0], lista[1]):
            lista.pop(1)
        else:
            lista.pop(0)
        ordem(lista, f)
    return lista[0]

#Exercicio 4.10
def filtrar_ordem(lista, f):
    pass

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    if len(lista) > 1:
        if ordem(lista[-1], lista[0]):
            l = lista[1:-1]
            l.insert(0, lista[-1])
            l.append(lista[0])
            lista=l
        lista= ordenar_seleccao(lista[:-1], ordem)+[lista[-1]]
    else:
        return lista
    return [lista[0]]+ordenar_seleccao(lista[1:], ordem)

