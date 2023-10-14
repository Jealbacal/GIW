# TODO: rellenar
# Asignatura: GIW
# Práctica XXXXXX
# Grupo: XXXXXXX
# Autores: XXXXXX
#
# Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
# sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
# de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
# de manera directa o indirecta. Declaramos además que no hemos realizado de manera
# deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
# resultados de los demás.

import csv

### Formato CSV
def lee_fichero_accidentes(ruta):

    with open(ruta, "r", encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')

        lista_dicc = list()
        keys = list()
        dicc = dict()

        for linea in reader:
            if reader.line_num == 1:
                keys = linea
            else:
                i = 0
                for item in linea:
                    dicc[keys[i]] = item
                    i += 1
                lista_dicc.append(dicc)

    return lista_dicc

    

def accidentes_por_distrito_tipo(datos):
    ...

def dias_mas_accidentes(datos):
    ...

def puntos_negros_distrito(datos, distrito, k):
    ...


#### Formato JSON
def leer_monumentos(json_file):
    ...

def subtipos_monumentos(monumentos):
    ...

def busqueda_palabras_clave(monumentos, palabras):
    ...

def busqueda_distancia(monumentos, calle, distancia):
    ...

for dicc in lee_fichero_accidentes("AccidentesBicicletas_2021.csv"):
    print("======================================================================================================")
    for item in dicc.items():
        print(item)

