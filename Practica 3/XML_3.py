from xml.etree import ElementTree as Et
from xml.etree.ElementTree import iterparse
from pprint import pprint


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
