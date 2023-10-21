

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
                self.name.append(html.unescape(content))
            
    parser=xml.sax.make_parser()        
    handler=NameHandler()
    parser.setContentHandler(handler)
    
    with open(filename,"r",encoding="utf-8") as fichero:
        parser.parse(fichero)

    # Return the extracted names
  
    return sorted(handler.name)   
            
#=======================================================
def subcategorias(filename):
    ...


def info_restaurante(filename, name):
    ...





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
            restaurante_nombre = html.unescape(name)
            l.append((dist, restaurante_nombre))

    l.sort(key=lambda x: x[0])
    return l
    

print(busqueda_cercania('restaurantes_v1_es_pretty.xml','Profesor José García Santesmases, Madrid, España', 3))


print("funciona")

print(nombres_restaurantes("restaurantes_v1_es.xml"))