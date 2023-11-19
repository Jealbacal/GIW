"""

Asignatura: GIW
Práctica 6
Grupo: 04
Autores:Jesús Alberto Barrios Caballero
        José Javier Carrasco Ferri
        Enrique Martín Rodríguez
        Felipe Ye Chen

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""
from datetime import datetime, timezone, timedelta
import requests

GOREST_URL="https://gorest.co.in"
USER_ENDPOINT="/public/v2/users"
COMMENTS_ENDPOINT="public/v2/comments"
TODOS_ENDPOINT="public/v2/todos"
#----TOKEN---------------------------------------------------------
# 01ddb601641b1808561a2a70a35c5f5c6d4562b56c7379defdd216d81b0f0b39
#------------------------------------------------------------------


#Ejercicio 1

def inserta_usuarios(datos, token):
    '''recibe una lista de diccionarios con informacion de varios usuarios y 
    almacena en el servicio web.Devuelve True si se añaden correctamente,
    False en caso contrario. '''

    sin_fallo = True
    for d in datos:
        r = requests.post(GOREST_URL+USER_ENDPOINT,
                        headers={'Authorization': f'Bearer {token}'},
                        data=d,
                        timeout=None
                    )
        if r.status_code / 100 != 2:
            sin_fallo = False

    return sin_fallo

#Ejercicio 2

def get_ident_email(email, token):
    '''Devuelve el identificador del usuario cuyo email es exactamente igual 
    al pasado por parametro,en caso contrario devuelve None.'''

    response = requests.get(GOREST_URL+USER_ENDPOINT,
    params={'access-token': token,
            'email':email
           },
    timeout=None)

    if response.status_code / 100 != 2:
        return "Error en la respuesta"

    if response.json() is None or len(response.json())<= 0:#si la respuesta es vacia
        return None

    return response.json()[0]["id"]

#Ejercicio 3

def borra_usuario(email, api_token):
    '''Elimina al usuario cuyo email es exactamente igual al pasado por parametro,
    en caso de exito devuleve True,en caso contrario devuelve False.'''
    id = get_ident_email(email,api_token)

    if id is None:
        return "Cannot find id"

    r = requests.delete(f'https://gorest.co.in/public/v2/users/{id}',
                headers={'Authorization': f'Bearer {api_token}'},
                timeout=None)

    if int(r.status_code/100) != 2:
        return False

    return True

#Ejercicio 4

def inserta_todo(email, token, title, due_on, status):
    '''Inserta una nueva tarea al usuario que tenga email exactamente igual al pasado por parametro,
    en caso de exito devuleve True,en caso contrario devuelve False.'''

    id=get_ident_email(email,token)
    if id is None:
        return False
    #accedo al endpoint del usuario con id
    todo_create_endpoint="/public/v2/users/{0}/todos".format(id)
    r = requests.post(GOREST_URL+todo_create_endpoint,
                headers={'Authorization': f'Bearer {token}'},
                data = {
                        "title":title,
                        "due_on":due_on,
                        "status":status},#datos del to-do
                timeout=None
                )

    if int(r.status_code/100) != 2:
        return False
    return True

#Ejercicio 5

def lista_todos(email, token):
    '''Devuelve una lista de diccionarios con la informacion de todas 
    las tareas asociadas al usuario que tenga email exactamente igual 
    al pasado por parametro, si no exixte ningun usuario con ese email
    devuleve una lista vacia.'''

    id=get_ident_email(email,token)

    if id is None:
        return []
    user_todo_endpoint="/public/v2/users/{0}/todos".format(id)
    r = requests.get(GOREST_URL+user_todo_endpoint,
                     params={'user_id' : id},
                     headers={'Authorization': f'Bearer {token}'},
                     timeout=None
                     )

    if r.status_code / 100 != 2:
        return []

    return r.json()

#Ejercicio 6

def lista_todos_no_cumplidos(email, token):
    '''Devulve una lista de diccionarios con las tareas no cumplidas del usuario
    que tenga email exactamente igual al pasado por parametro'''
    id=get_ident_email(email,token)
    if id is None:
        return []
    user_todo_endpoint="/public/v2/users/{0}/todos".format(id)
    response = requests.get(GOREST_URL+user_todo_endpoint,
                     params={'user_id' : id},
                     headers={'Authorization': f'Bearer {token}'},
                     timeout=None
                     )
    result=[]
    if int(response.status_code/100)!=2:
        return []
    if len(response.json())<=0 :
        return []
    for r in response.json():

        rtime = datetime.fromisoformat(r["due_on"])#tiempo devuelto
        currtime=datetime.now(timezone(timedelta(hours=1)))#tiempo actual españa UTC+1

        if currtime > rtime and r["status"]=="pending":#si esta pending o todavia le queda tiempo
            result.append(r)

    return result
