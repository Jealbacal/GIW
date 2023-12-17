"""
Asignatura: GIW
Práctica 9
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


from flask import Flask, request, session, render_template, send_file, make_response
from mongoengine import connect, Document, StringField, EmailField
from os import urandom
from hashlib import sha256
# Resto de importaciones
from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher
import os
import pyotp
import base64
import qrcode


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
    hash_passwd = ph.hash(pssw + PIMIENTA)
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
#     - Uso de pimienta, añadiendo una capa extra de seguridad con un secreto propio por si se filtran las contraseñas
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
    
    hasher = PasswordHasher(**options)
    
    user = User.objects(user_id=nombre).first()

    try:
        hasher.verify(user.passwd, old_passwd + PIMIENTA)
    except VerifyMismatchError:
        return "Usuario o contraseña incorrecto"

    if user is None:
        return "Usuario o contraseña incorrecto"
    user.passwd = hashpassArgon(new_passwd) # BORRAR COMMENT LUEGO, ¡acordarse de actualizar la contrasena!
    user.save()
    return f"La contraseña de {nombre} ha sido cambiado"
 
           
@app.route('/login', methods=['POST'])
def login():
    
    nombre=request.form.get("nickname")
    pssw=request.form.get("password")

    hasher = PasswordHasher(**options)
    
    user = User.objects(user_id=nombre).first()

    try:
        hasher.verify(user.passwd, pssw + PIMIENTA)
    except VerifyMismatchError:
        return "Usuario o contraseña incorrecto"

    if user is None:
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
    #hash_pssw="abc123"#a mi no me va el argon
    secret_b32 = pyotp.random_base32()

    usuario=User(user_id=nombre,full_name=nombreC,country=pais,email=mail,passwd=hash_pssw)
    usuario.save()

    url = pyotp.utils.build_uri(secret_b32,nombre,None,"localhost","base32",6,10000,None)
    # url = pyotp.utils.build_uri(secret_b32,nombre) # sin parametros opcionalwes

    # Codigo QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    #SOL felipe render template---------------------------------------------------------------------

    # Save the QR code image (optional)
    img.save(os.path.join("static", f'qr_image_{nombre}.png'))

    # Render the template with the QR code
    return render_template('qr.html', qr_code='qr_image.png',username=nombre, secreto=secret_b32)

    #-----------------------------------------------------------------------------------------------
    
    #Sol JJ base64----------------------------------------------------------------------------------
    # img_path = f"codigos/qr{nombre}.png"

    # img.save(img_path)

    # with open(img_path, 'rb') as img_file:
    #     img_data = img_file.read()

    # img_64 = base64.b64encode(img_data).decode('utf-8')

    # return f"Bienvenido {nombre}, tu secreto es: {secret_b32} <br><img src=\"data:image/png;base64,{img_64}\"/>"

    #------------------------------------------------------------------------------------------------


@app.route('/login_totp', methods=['POST'])
def login_totp():

    nombre=request.form.get("nickname")
    pssw=request.form.get("password")
    totp_user=request.form.get("totp")
    
    hasher = PasswordHasher(**options)
    
    user = User.objects(user_id=nombre).first()

    try:
        hasher.verify(user.passwd, pssw + PIMIENTA)
    except VerifyMismatchError:
        return "Usuario o contraseña incorrecto"

    totp = pyotp.TOTP(user.totp_secret)
    totp.now()

    if user is None or not totp.verify(totp_user):
        return "Usuario o contraseña incorrecto"
    return f"Bienvenido {nombre}"
  

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
