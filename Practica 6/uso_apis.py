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
GOREST_URL="https://gorest.co.in"
USER_ENDPOINT="/public/v2/users"
COMMENTS_ENDPOINT="public/v2/comments"
TODOS_ENDPOINT="public/v2/todos"
#----TOKEN---------------------------------------------------------
# 01ddb601641b1808561a2a70a35c5f5c6d4562b56c7379defdd216d81b0f0b39
#------------------------------------------------------------------

import requests
from pprint import pprint
from datetime import datetime, timezone, timedelta

#Ejercicio 1

def inserta_usuarios(datos, token):

    for d in datos:
        r = requests.post(GOREST_URL+USER_ENDPOINT, 
                        headers={'Authorization': f'Bearer {token}'},
                        data=d
                    )
        pprint(r.status_code)
        if (r.status_code / 100 != 2): 
            pprint(r.json())
            return False

    return True

#Ejercicio 2

def get_ident_email(email, token):
    
    response = requests.get( GOREST_URL+USER_ENDPOINT,
    params={'apikey': {token},
            'email':email
           },
          )
   
    if (response.status_code / 100 != 2): return "Error en la respuesta"
    
    if response.json()is None or len(response.json())<= 0:#si la respuesta es vacia
        return None

    return response.json()[0]["id"]

#Ejercicio 3               

def borra_usuario(email, api_token):
    id = get_ident_email(email,api_token)

    if(id is None):
        return "Cannot find id"
    else:
        r = requests.delete(f'https://gorest.co.in/public/v2/users/{id}',
                    headers={'Authorization': f'Bearer {api_token}'})
        
        print(r.status_code)
        if int(r.status_code/100) != 2: return False

    return True

#Ejercicio 4

def inserta_todo(email, token, title, due_on, status):
    
    id=get_ident_email(email,token)
    if id is None:
        return False
    
    TODO_CREATE_ENDPOINT="/public/v2/users/{0}/todos".format(id)#accedo al endpoint del usuario con id 
    r = requests.post(GOREST_URL+TODO_CREATE_ENDPOINT,
                headers={'Authorization': f'Bearer {token}'},
                data = {
                        "title":title,
                        "due_on":due_on,
                        "status":status}#datos del to-do
                )
  
    if int(r.status_code/100) != 2:
        return False
    return True



#Ejercicio 5

def lista_todos(email, token):
    
    id=get_ident_email(email,token)

    if id is None: return []
    USER_TODO_ENDPOINT="/public/v2/users/{0}/todos".format(id)
    r = requests.get(GOREST_URL+USER_TODO_ENDPOINT,
                     params={'user_id' : id},
                     headers={'Authorization': f'Bearer {token}'}
                     )
    
    if (r.status_code / 100 != 2): return []
    
    return r.json()

#Ejercicio 6

def lista_todos_no_cumplidos(email, token):
    id=get_ident_email(email,token)
    if id is None:
        return []
    USER_TODO_ENDPOINT="/public/v2/users/{0}/todos".format(id)
    response = requests.get( GOREST_URL+USER_TODO_ENDPOINT,
    params={'apikey': {token},
            #vacio para que devuelva todo
           },
          )
    result=[]
    if int(response.status_code/100)!=2:
        return []
    if len(response.json())<=0 :
        return []
    for r in response.json():
        
        rtime = datetime.fromisoformat(r["due_on"])#tiempo devuelto
        currtime=datetime.now(timezone(timedelta(hours=1)))#tiempo actual españa UTC+1
        
        if rtime>currtime or r["due_on"]=="pending":#si esta pending o todavia le queda tiempo
            result.append(r)

    return result

# Testeo
with open('token_gorest.txt','r',encoding='utf8') as f:
    TOKEN_GOREST = f.read().strip()

#Teste ej 1
# print(borra_usuario("evaa@gmail.com", TOKEN_GOREST))
# print(borra_usuario("anaa@gmail.com", TOKEN_GOREST))
# print(borra_usuario("facu@gmail.com", TOKEN_GOREST))

# u1 = {'name': 'Eva', 'email': 'evaa@gmail.com', 'gender': 'female', 'status': 'inactive'}
# u2 = {'name': 'Ana', 'email': 'anaa@gmail.com', 'gender': 'female', 'status': 'active'}
# u3 = {'name': 'Pepe', 'email': 'pepee@gmail.com', 'gender': 'female', 'status': 'inactive'}

# print(inserta_usuarios([u1,u2], TOKEN_GOREST))
#print(inserta_usuarios([u2,u3], TOKEN_GOREST))

pprint(lista_todos("upendra_khan@hartmann.test",TOKEN_GOREST))


#with open('token_gorest.txt', 'r', encoding='utf8') as f:
#    TOKEN_GOREST = f.read().strip()

# USER="upendra_khan@hartmann.test"#para cambiar mas facil 
# pprint(get_ident_email(USER,TOKEN_GOREST))
# pprint(inserta_todo(USER,TOKEN_GOREST,"TODO NUEVO","2024-07-28 11:30","pending"))
# pprint(lista_todos_no_cumplidos(USER, TOKEN_GOREST))

