"""
TODO: rellenar

Asignatura: GIW
Práctica 6
Grupo: XXXXXXX
Autores: XXXXXX 

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

#----TOKEN---------------------------------------------------------
# 01ddb601641b1808561a2a70a35c5f5c6d4562b56c7379defdd216d81b0f0b39
#------------------------------------------------------------------

import requests
from pprint import pprint

#Ejercicio 1

def inserta_usuarios(datos, token):

    for d in datos:
        r = requests.post('https://gorest.co.in/public/v2/users',
                    headers={'Authorization': f'Bearer {token}'},
                    data = d
                    )
        if (r.status_code % 100 != 2): return False

    return True

#Ejercicio 2

def get_ident_email(email, token):
    ...

#Ejercicio 3

def borra_usuario(email, api_token):
    ...

#Ejercicio 4

def inserta_todo(email, token, title, due_on, status):
    ...

#Ejercicio 5

def lista_todos(email, token):
    ...

#Ejercicio 6

def lista_todos_no_cumplidos(email, token):
    ...

# Testeo
with open('token_gorest.txt','r',encoding='utf8') as f:
    TOKEN_GOREST = f.read().strip()

    #Teste ej 1
    u1 = {'name': 'Eva', 'email': 'eva@gmail.com', 'gender': 'female', 'status': 'inactive'}
    u2 = {'name': 'Ana', 'email': 'ana@gmail.com', 'gender': 'female', 'status': 'active'}
    u3 = {'name': 'Pepe', 'email': 'pepe@gmail.com', 'gender': 'female', 'status': 'inactive'}

    print(inserta_usuarios([u1,u2], TOKEN_GOREST))
    print(inserta_usuarios([u2,u3], TOKEN_GOREST))
