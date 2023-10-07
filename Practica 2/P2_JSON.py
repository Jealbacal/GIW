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


### Formato CSV
# def lee_fichero_accidentes(ruta):
#     ...

# def accidentes_por_distrito_tipo(datos):
#     ...

# def dias_mas_accidentes(datos):
#     ...

# def puntos_negros_distrito(datos, distrito, k):


# Formato JSON
import json
from geopy.geocoders import Nominatim
from geopy import distance


def leer_monumentos(json_file):

    print("Opening json file with name\n", json_file)

    with open(json_file, 'r', encoding="utf8") as Fichero:
        data = json.load(Fichero)
        diccionario = dict()
        lista = []
        for d in data["@graph"]:  # datos
            diccionario = dict()
            for key, value in d.items():  # clave valor
                # print("Clave",key,"Valor",value,"\n")
                diccionario[key] = value
            lista.append(diccionario)
    return lista


def subtipos_monumentos(monumentos):
    lista_subtipos = []
    for a in monumentos:
        tipo = a['subtipo']
        if (tipo not in lista_subtipos):
            lista_subtipos.append(tipo)

    lista_subtipos.sort()
    return lista_subtipos


def busqueda_palabras_clave(monumentos, palabras):
    longitud = len(palabras)
    lista = []
    for a in monumentos:
        nombre = a['nombre']
        desc = a['descripcion']
        contador = 0
        for palabra in palabras:

            if (palabra in nombre or palabra in desc):
                contador += 1

            if (contador == longitud):
                lista.append((nombre, a['distrito']))
    return lista


def location(calle):
    geolocator = Nominatim(user_agent="Ejemplo")
    location = geolocator.geocode(calle, addressdetails=True)
    return (location.latitude, location.longitude)


def busqueda_distancia(monumentos, calle, distancia):
    localizacion = location(calle)
    lista = []
    for a in monumentos:
        loc = (a['latitud'], a['longitud'])
        dist = distance.distance(localizacion, loc).km
        if (dist < distancia):
            lista.append((a['nombre'], a['subtipo'], dist))

    return lista


# leer_monumentos("monumentos_madrid.json")
print("=================")
lista_monumentos = leer_monumentos("monumentos_madrid.json")

lista_subtipos = subtipos_monumentos(lista_monumentos)
for a in lista_subtipos:
    print(a, "\n")
print("=================")
palabras = ['escultura', 'agua']
lista_busqueda = busqueda_palabras_clave(lista_monumentos, palabras)

for a in lista_busqueda:
    print(a, "\n")

print("=================")
lista_distancia = busqueda_distancia(
    lista_monumentos, "Profesor José García Santesmases, Madrid,España", 1)

for a in lista_distancia:
    print(a, "\n")
