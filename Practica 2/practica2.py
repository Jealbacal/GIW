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


with open("AccidentesBicicletas_2021.csv", 'r', newline='', encoding='utf8') as file:
    datos = csv.DictReader(file, delimiter=';')
    lista = list(datos)
    accidentes_por_distrito_tipo(lista)
    # pprint(lista[:10])
