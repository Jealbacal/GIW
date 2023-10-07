# TODO: rellenar
# Asignatura: GIW
# Práctica 2
# Grupo: 04
# Autores:  Jesús Alberto Barrios Caballero
#           José Javier Carrasco Ferri
#           Enrique Martín Rodríguez
#           Felipe Ye Chen
#
# Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
# sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
# de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
# de manera directa o indirecta. Declaramos además que no hemos realizado de manera
# deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
# resultados de los demás.

import json
import csv
from geopy.geocoders import Nominatim
from geopy import distance

# Formato CSV


def lee_fichero_accidentes(ruta):
    with open("AccidentesBicicletas_2021.csv", encoding="utf-8") as archivo:
        accidentes = []

        for linea in archivo:
            linea = linea.rstrip("\n")
            columna = linea.split(";")
            cod_distrito = columna[5]
            cod_lesividad = columna[13]
            coordeanda_x_utm = columna[15]
            coordeanda_y_utm = columna[16]
            distrito = columna[6]
            estado_meteorologico = columna[8]
            fecha = columna[1]
            hora = columna[2]
            localizacion = columna[3]
            num_expediente = columna[0]
            numero = columna[4]
            positiva_alcohol = columna[17]
            positiva_droga = columna[18]
            rango_edad = columna[11]
            sexo = columna[12]
            tipo_accidente = columna[7]
            tipo_lesividad = columna[14]
            tipo_persona = columna[10]
            tipo_vehiculo = columna[9]
            accidentes.append({

                "cod_distrito": cod_distrito,
                "cod_lesividad ":  cod_lesividad,
                "coordeanda_x_utm": coordeanda_x_utm,
                "coordeanda_y_utm": coordeanda_y_utm,
                "distrito": distrito,
                "estado_meteorologico":  estado_meteorologico,
                "fecha": fecha,
                "hora": hora,
                "localizacion": localizacion,
                "num_expediente": num_expediente,
                "numero": numero,
                "positiva_alcohol":  positiva_alcohol,
                "positiva_droga": positiva_droga,
                "rango_edad": rango_edad,
                "sexo": sexo,
                "tipo_accidente": tipo_accidente,
                "tipo_lesividad":  tipo_lesividad,
                "tipo_persona": tipo_persona,
                "tipo_vehiculo": tipo_vehiculo

            })

        return accidentes[1::]


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

    return result


def dias_mas_accidentes(datos):
    ...


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


# Formato JSON
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
