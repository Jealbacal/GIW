# TODO: rellenar
# Asignatura: GIW
# Práctica 5
# Grupo: 04
# Autores: Jesús Alberto Barrios Caballero
#          José Javier Carrasco Ferri
#          Enrique Martín Rodríguez
#          Felipe Ye Chen
         
#
# Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
# sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
# de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
# de manera directa o indirecta. Declaramos además que no hemos realizado de manera
# deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
# resultados de los demás.

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = 'https://books.toscrape.com/'


# APARTADO 1 #
def explora_categoria(url):
    """ A partir de la URL de la página principal de una categoría, devuelve el nombre
        de la categoría y el número de libros """
    response2 = requests.get(url)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    libros = soup2.select_one('form strong')
    nombre = soup2.find('h1')
    
    return((nombre.text, int( libros.text))) # una vez  en la pagina de cada categoria se obtinien el nombre y el numero de libros


def categorias():
    """ Devuelve una lista de parejas (nombre, número libros) de todas las categorías """
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    categorias1 = []
    
    for categoria in soup.find('ul', class_='nav-list').find_all('a')[1:]:#de la lsita en la que estan todas las categorias quiero todas
                                                                            #menos la primera que es el general de book        
        new_url = URL + categoria['href']#ahora tengo que ir al enlace de los libros de cada categoria y contarlos
        
        categorias1.append(explora_categoria(new_url))#lo devuevle tal cual la salida pero al transformar en conjunto pierde el orden ( como pide el enunciado)

    return set(categorias1)


# APARTADO 2 #
def url_categoria(nombre):
    """ Devuelve la URL de la página principal de una categoría a partir de su nombre (ignorar
        espacios al principio y final y también diferencias en mayúsculas/minúsculas) """
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    etiquetas = soup.find('ul', class_='nav-list').find_all('a')[1:]
    for etiqueta in etiquetas:
        if etiqueta.text.strip().lower() == nombre.lower().strip(): # se asgura de quitar los espacios al principio y al final, a su vez se lleva todo a minusculas.
            return URL + etiqueta.get('href')

    return  None  


def todas_las_paginas(url):
    """ Sigue la paginación recopilando todas las URL *absolutas* atravesadas """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    result=[]
    result.append(url)
    siguiente= soup.find('li',class_='next')
    while siguiente is not None:         # se busca el hipervinculo del boton 'next' hasta que este no exista, si se encuentra se usa la funcion urljoin para obtener la direccion absoluta
        siguiente_href =siguiente.find('a').get('href')
        newUrl= urljoin(url,siguiente_href)
        result.append(newUrl)
        response2 = requests.get(newUrl)
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        siguiente= soup2.find('li',class_='next')
    
    return result

def numeros(numero):
    """ funcion auxilar para transfomar los numeros escritos en lenguaje natural a su forma numerica"""
    if(numero == 'One'):
        return 1
    elif(numero == 'Two'):
        return 2
    elif(numero == 'Three'):
        return 3
    elif(numero == 'Four'):
        return 4
    elif(numero == 'Five'):
        return 5
    else:
        return None

def libros_categoria(nombre):
    """ Dado el nombre de una categoría, devuelve una lista (titulo, precio, valoracion), donde el
        precio será un número real y la valoración un número natural. Los libros de esta lista estarán
        ordenados de mayor a menor valoración"""

    urlcategoria = url_categoria(nombre)
    links=todas_las_paginas(urlcategoria)
    conjunto = set()
    for link in links:  # por cada link conseguido de la funcion "todas_las_paginas" se busca todas las componentes que contiene la infomarcion del libro
        reponse =requests.get(link)
        soup = BeautifulSoup(reponse.text,'html.parser')
        libros = soup.find_all('li',class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
        
        for libro in libros:     # una vez tenido una lista con todas las componentes de los libros se recorre para sacar la informacion pedida
            
            info =libro.find('article',class_='product_pod')
            nombre = info.find('h3').find('a').get('title')
            precio = float(info.find('div', class_="product_price").find('p',class_ ='price_color').text.strip()[2:])
            valoracion = numeros(info.find('p')['class'][1])
            info_libro = (nombre,precio,valoracion)
            conjunto.add(info_libro)


    return conjunto
