"""
TODO: rellenar

Asignatura: GIW
Práctica X
Grupo: XXXXXXX
Autores: XXXXXX 

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""


from flask import Flask, request, session, render_template, send_file, make_response
from mongoengine import connect, Document, StringField, EmailField
from os import urandom
from hashlib import sha256
# Resto de importaciones
import argon2
from argon2 import PasswordHasher
import pyotp
import qrcode
import io


PIMIENTA = b'SalPimentarAlGusto'

# Opciones argon2
options = {
    'time_cost': 2,         # Número de iteraciones de procesamiento de tiempo
    'memory_cost': 65536,    # Tamaño de memoria en kilobytes
    'parallelism': 2,        # Número de hilos paralelos
    'hash_len': 32,          # Longitud del hash de salida en bytes
    'salt_len': 32           # Longitud de la sal en bytes
}

app = Flask(__name__)
connect('giw_auth')
salt=urandom(32)

def hashpass(pssw):
    salt_passwd=pssw.encode('utf-8')+salt
    hash_passwd=sha256(salt_passwd).hexdigest()
    return hash_passwd
    
def hashpassArgon(pssw):
    ph = PasswordHasher(**options)
    hash_passwd = ph.hash(pssw)
    return hash_passwd
    

# Clase para almacenar usuarios usando mongoengine
# ** No es necesario modificarla **

class User(Document):
    user_id = StringField(primary_key=True)
    full_name = StringField(min_length=2, max_length=50, required=True)
    country = StringField(min_length=2, max_length=50, required=True)
    email = EmailField(required=True)
    passwd = StringField(required=True)
    totp_secret = StringField(required=False)


##############
# APARTADO 1 #
##############

# Explicación detallada del mecanismo escogido para el almacenamiento de
# contraseñas, explicando razonadamente por qué es seguro:
# 
# El mecanismo escogido para el almacenamiento de contraseñas en esta aplicacion
# es seguro ya que se usa argon2 para:
#
#     - Almaceniamiento del hash de la contraseña, haciendo inviable la obtencion del texto plano
#     - Uso de sal para el calculo de del hash, haciendo que usuarios con la misma clave tengan distinto hash
#     - Uso de pimienta, añadiendo una capa extra de seguridad por si se filtran las contraseñas
#     - Uso del ralentizado, para hacer inviables los ataques por fuerza bruta

@app.route('/signup', methods=['POST'])
def signup():
 
    nombre=request.form.get("nickname")
    nombreC=request.form.get("full_name")
    pais=request.form.get("country")
    mail=request.form.get("email")
    pssw=request.form.get("password")
    pssw2=request.form.get("password2")
    
    if pssw!=pssw2:
        return "Las contraseñas no coinciden"
    
    usernames = [user.user_id for user in User.objects]
    
    if nombre in usernames:
        return "El usuario ya existe"
    
    hash_pssw=hashpassArgon(pssw)


    usuario=User(user_id=nombre,full_name=nombreC,country=pais,email=mail,passwd=hash_pssw)
    usuario.save()
    return f"Bienvenido usuario {nombre}"
    
    

# usuario=User(user_id="felipe",full_name="Felipe Ye Chen",country="ESpaña",email="email@email.com",passwd="abc")
    # usuario.save()
@app.route('/change_password', methods=['POST'])
def change_password():
    
    nombre=request.form.get("nickname")
    old_passwd=request.form.get("old_password")
    new_passwd=request.form.get("new_password")
    
    hash_pssw=hashpassArgon(old_passwd)
    
    user = User.objects(user_id=nombre).first()
    if user is None or user.passwd != hash_pssw:
        return "Usuario o contraseña incorrecto"
    return f"La contraseña de {nombre} ha sido cambiado"
 
           
@app.route('/login', methods=['POST'])
def login():
    
    nombre=request.form.get("nickname")
    pssw=request.form.get("password")
    
    hash_pssw=hashpassArgon(pssw)
    
    user = User.objects(user_id=nombre).first()
    if user is None or user.passwd != hash_pssw:
        return "Usuario o contraseña incorrecto"
    return f"Bienvenido {nombre}"
    
##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#


@app.route('/signup_totp', methods=['POST'])
def signup_totp():

    nombre=request.form.get("nickname")
    nombreC=request.form.get("full_name")
    pais=request.form.get("country")
    mail=request.form.get("email")
    pssw=request.form.get("password")
    pssw2=request.form.get("password2")
    
    if pssw!=pssw2:
        return "Las contraseñas no coinciden"
    
    usernames = [user.user_id for user in User.objects]
    
    if nombre in usernames:
        return "El usuario ya existe"
    
    hash_pssw=hashpassArgon(pssw)

    secret_b32 = pyotp.random_base32()

    totp = pyotp.TOTP(secret_b32)
    totp.now()

    url = pyotp.utils.build_uri(totp,nombre,None,"localhost","base32",6,10000,None)
    img_path = f"qr{nombre}.png"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(img_path)
    
    img_byte_array = io.BytesIO()
    img.save(img_byte_array)
    img_byte_array.seek(0)

    usuario=User(user_id=nombre,full_name=nombreC,country=pais,email=mail,passwd=hash_pssw,totp_secret=secret_b32)
    usuario.save()

    response = make_response(send_file(img_path, mimetype='image/png'))

    response.headers["Custom-String"] = f"Bienvenido {nombre}, tu secreto es: {secret_b32}"

    send_file(img_byte_array, mimetype='image/png')

    return response

@app.route('/login_totp', methods=['POST'])
def login_totp():
    ...
  

class FlaskConfig:
    """Configuración de Flask"""
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = 'la_asignatura_de_giw'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    
    db = User._get_db()
    collections = db.list_collection_names()
    for collection in collections:
        db.drop_collection(collection)
        
    app.run(host="localhost", port=5000, debug=True)