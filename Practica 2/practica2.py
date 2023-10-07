# Ejercicio 2

import csv
from pprint import pprint


def accidentes_por_distrito_tipo(datos):
    lista = []
    result = {}
    for linea in datos:
        distrito = linea.get('distrito')
        accidente = linea.get('tipo_accidente')
        aux = (distrito, accidente)
        lista.append(aux)
        lista.sort()

    for tupla in lista:
        result[tupla] = lista.count(tupla)

    pprint(result)
    return result


def puntos_negros_distrito(datos, distrito, k):
    distritoList = []
    result = []
    distritoList = [x for x in datos if x.get('distrito') == distrito]
    localidades = [x.get('localizacion') for x in distritoList]

    for linea in distritoList:
        local = linea.get('localizacion')
        tupla = (local, localidades.count(local))
        if tupla not in result:
            result.append(tupla)

    result.sort(key=lambda x: (x[1], x[0]), reverse=True)
    result = result[:k]
    pprint(result)


with open("AccidentesBicicletas_2021.csv", 'r', newline='', encoding='utf8') as file:
    datos = csv.DictReader(file, delimiter=';')
    lista = list(datos)
    # accidentes_por_distrito_tipo(lista)
    puntos_negros_distrito(lista, 'MONCLOA-ARAVACA', 16)
    # pprint(lista[:10])
