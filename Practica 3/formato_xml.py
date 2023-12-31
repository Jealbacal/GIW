# Asignatura: GIW
# Práctica 3
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

import xml.sax
import html
from xml.etree import ElementTree
from geopy import distance
from geopy.geocoders import Nominatim


def nombres_restaurantes(filename):
    class NameHandler(xml.sax.ContentHandler):

        def __init__(self):
            self.curr_path = []
            self.name = []

        def startElement(self, name, attrs):
            self.curr_path.append(name)

        def endElement(self, name):
            self.curr_path.pop()

        def characters(self, content):
            if self.curr_path == ["serviceList", "service", "basicData", "name"]:
                # escapamos el nombre que nos interesa y los espacios a la izquierda
                self.name.append(html.unescape(content.lstrip()))

    parser = xml.sax.make_parser()
    handler = NameHandler()
    parser.setContentHandler(handler)

    with open(filename, "r", encoding="utf-8") as fichero:
        parser.parse(fichero)

    # Return the extracted names

    return sorted(handler.name)


def subcategorias(filename):

    class Ejercicio2Handler(xml.sax.ContentHandler):

        lista = []
        categoria = ""
        subcategoria = ""
        is_num = False  # booelano para diferenciar item numerico de item de texto

        def __init__(self):
            self.curr_path = []
            self.name = []

        def startElement(self, name, attrs):
            if name == "item":  # Escapar cadenas de numeros en en item subcategorias
                if attrs["name"] == "idSubCategoria":
                    self.is_num = True
                else:
                    self.is_num = False

            self.curr_path.append(name)

        def endElement(self, name):
            self.curr_path.pop()

        def characters(self, content):
            # Si llegamos al item de categoria
            if len(self.curr_path) >= 2 and self.curr_path[-2:] == ["categoria", "item"]:
                self.categoria = content
            # Si llegamos al item de subcategoria
            if len(self.curr_path) >= 4 and self.curr_path[-4:] == ["categoria", "subcategorias", "subcategoria", "item"]:
                if (not self.is_num):
                    self.subcategoria = content
                    self.lista.append((self.categoria, self.subcategoria))

    parser = xml.sax.make_parser()
    parser.setContentHandler(Ejercicio2Handler())

    with open(filename, "r", encoding="utf-8") as fichero:
        parser.parse(fichero)

    return Ejercicio2Handler.lista


def info_restaurante(filename, name):
    arbol = ElementTree.parse(filename)
    # funcion para escapar los contenidos
    def escapar(x): return html.unescape(x) if x is not None else None
    # va recorriendo el arbol buscando por la ruta especificada
    for nodo in arbol.findall("./service"):
        nombre = escapar(nodo.find('./basicData/name').text)
        if nombre == name:
            # se va generando el diccionario segun los elementos que se piden con sus rutas correspondientes
            result = {
                'descripcion': escapar(nodo.find('./basicData/body').text),
                'email': escapar(nodo.find('./basicData/email').text),
                'horario': escapar(html.unescape(nodo.find("./extradata/item/[@name='Horario']").text)),
                'nombre': nombre,
                'phone': escapar(nodo.find('./basicData/phone').text),
                'web': escapar(nodo.find('./basicData/web').text)

            }
            return result
        # si no encuentra el restaurante devuleve None
    return None


def location(lugar):
    geolocator = Nominatim(user_agent="Ejemplo")
    location = geolocator.geocode(lugar, addressdetails=True)
    return (location.latitude, location.longitude)


def busqueda_cercania(filename, lugar, n):
    l = []
    arbol = ElementTree.parse(filename)
    raiz = arbol.getroot()

    sitio = location(lugar)
    # Voy metiendome y buscando lo que necesito en este caso las distancias de cada restaurante y
    for service in raiz.iter('service'):
        # el nombre, para la distancia almacenamos latitud y longitud y usamos la funcion de la P2 con geopy
        name = service.find('.//name').text
        latitude = float(service.find('.//latitude').text)
        longitude = float(service.find('.//longitude').text)
        coords = (latitude, longitude)
        dist = distance.distance(sitio, coords).km

        # Si la distancia es menor o igual a n kilómetros, agregar a la lista
        if dist <= n:
            r_name = html.unescape(name)
            l.append((dist, r_name))

    l.sort(key=lambda x: x[0])  # ordena
    return l
