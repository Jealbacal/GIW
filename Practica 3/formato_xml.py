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

import pprint
import xml.sax
import html
from xml.etree import ElementTree
from geopy import distance
from geopy.geocoders import Nominatim
from xml.etree import ElementTree as Et
from xml.etree.ElementTree import iterparse



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
                self.name.append(html.unescape(content))
            
    parser=xml.sax.make_parser()        
    handler=NameHandler()
    parser.setContentHandler(handler)
    
    with open(filename,"r",encoding="utf-8") as fichero:
        parser.parse(fichero)

    # Return the extracted names
  
    return sorted(handler.name)  


print(nombres_restaurantes("restaurantes_v1_es.xml")) 

def subcategorias(filename):

    class Ejercicio2Handler(xml.sax.ContentHandler):

        lista = []
        categoria = ""
        subcategoria = ""
        
        def __init__(self):
            self.curr_path = [] 
            self.name = []

        def startElement(self, name, attrs):
            self.curr_path.append(name)
            
            
            if name == "item":
                if attrs["name"] != "idCategoria" or attrs["name"] != "idSubCategoria":
                    self.curr_path.append(name)
            else:
                self.curr_path.append(name)

        def endElement(self, name):
            self.curr_path.pop()

        def characters(self, content):
            if len(self.curr_path) >= 2 and self.curr_path[-2:] == ["categoria","item"]:
                self.categoria = content
            if len(self.curr_path) >= 4 and self.curr_path[-4:] == ["categoria","subcategorias","subcategoria","item"]:
                self.subcategoria = content
                self.lista.append((self.categoria,self.subcategoria))
    
    parser = xml.sax.make_parser()
    parser.setContentHandler(Ejercicio2Handler())
    
    with open(filename,"r",encoding="utf-8") as fichero:
        parser.parse(fichero)

    return Ejercicio2Handler.lista


for i in subcategorias("restaurantes_v1_es_pretty.xml"):
    print(i)


def info_restaurante(filename, name):
    arbol = Et.parse(filename)

    for nodo in arbol.findall("./service"):
        nombre = nodo.find('./basicData/name').text
        if nombre == name:
            result = {
                'descripcion': nodo.find('./basicData/body').text,
                'email': nodo.find('./basicData/email').text,
                'horario': nodo.find("./extradata/item/[@name='Horario']").text,
                'nombre': nombre,
                'phone': nodo.find('./basicData/phone').text,
                'web': nodo.find('./basicData/web').text

            }
            return result
    return None


pprint(info_restaurante("restaurantes_V1_es_pretty.xml", "Hasaku Nikei"))

def location(lugar):
    geolocator = Nominatim(user_agent="Ejemplo")
    location = geolocator.geocode(lugar, addressdetails=True)
    return (location.latitude, location.longitude)

def busqueda_cercania(filename, lugar, n):
    l = []
    arbol= ElementTree.parse(filename)
    raiz = arbol.getroot()
    
    sitio = location(lugar)
    for service in raiz.iter('service'): #Voy metiendome y buscando lo que necesito en este caso las distancias de cada restaurante y 
                                            #el nombre
        name = service.find('.//name').text
        latitude = float(service.find('.//latitude').text)
        longitude = float(service.find('.//longitude').text)
        coords = (latitude, longitude)
        dist = distance.distance(sitio,coords).km
        
        # Si la distancia es menor o igual a n kilómetros, agregar a la lista
        if dist <= n:
            r_name = html.unescape(name)
            l.append((dist, r_name))

    l.sort(key=lambda x: x[0])
    return l
    

print(busqueda_cercania('restaurantes_v1_es_pretty.xml','Profesor José García Santesmases, Madrid, España', 3))


