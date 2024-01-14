"""
Asignatura: GIW
Práctica 10
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

from flask import Flask, request

# Resto de importaciones
import requests
import jwt


app = Flask(__name__)


# Credenciales
CLIENT_ID = '975211704103-er0fm5sk122t5oogcbsdesa0rgf5o9ur.apps.googleusercontent.com'
CLIENT_SECRET = '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'

REDIRECT_URI = 'http://localhost:5000/token'

# Fichero de descubrimiento para obtener el 'authorization endpoint' y el
# 'token endpoint'
DISCOVERY_DOC = 'https://accounts.google.com/.well-known/openid-configuration'

def exchange_code_for_id_token(code):
    """Canjea el código de autorización por un id_token.

    Realiza una petición POST al token endpoint de Google para canjear el código de autorización
    por un id_token. El id_token es un JWT firmado por Google que contiene información del usuario.
    """

    token_endpoint = 'https://oauth2.googleapis.com/token'
    payload = {  # Datos necesarios para canjear el código de autorización por un id_token
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_endpoint, data=payload, timeout=5)  # Realizamos la petición POST
    if response.status_code == 200:
        token_data = response.json()  # Obtenemos el id_token
        id_token = token_data.get('id_token')  # Extraemos el id_token
        return id_token

    return None


def extract_email_from_id_token(id_token):
    """Extrae el email del id_token.

    Dado un id_token (JWT) firmado por Google, extrae el email del usuario.
    """
    # Decodificamos el JWT sin validar la firma (nos fiamos de Google)
    id_token_decoded = jwt.decode(id_token, options={"verify_signature": False})
    return id_token_decoded.get('email')  # Extraemos el email del JWT


# Rutas
@app.route('/login_google', methods=['GET'])
def login_google():
    """
    Redirige al usuario a la página de autenticación de Google.

    Genera una página HTML con un enlace o un botón que redirige al usuario a la página de
    autenticación delegada de Google. Esta petición debe contener las credenciales necesarias de
    nuestra aplicación web.
    """

    auth_url = f'https://accounts.google.com/o/oauth2/v2/auth?' \
            f'client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}'\
            f'&response_type=code&scope=openid%20email'
    return f'<html><body><a href="{auth_url}"><button>Login with Google</button></a></body></html>'


@app.route('/token', methods=['GET'])
def token():
    """Obtiene el token de acceso y redirige al usuario a la página de inicio.

    Recibe la petición del usuario redirigida desde Google con el código temporal que deberemos
    canjear por un id_token. 
    Por tanto, en las credenciales de nuestra aplicación deberemos configurar
    el redirect_uri a http://localhost:5000/token tal y como aparece en el esqueleto. El id_token
    que obtendremos será un JWT firmado por Google con la información del usuario. Como este
    JWT lo hemos obtenido a través de una conexión HTTPS con Google no es necesario validar la
    firma, únicamente extraer la dirección de e-mail. Finalmente se generará una página HTML de
    bienvenida con el mensaje Bienvenido <e-mail>
    """

    code = request.args.get('code')  # Código de autorización
    if code:

        # Canjeamos el código por un id_token
        id_token = exchange_code_for_id_token(code)

        # Extraemos el email del id_token
        email = extract_email_from_id_token(id_token)

        # Generamos la página de bienvenida
        return f'<html><body><h1>Welcome {email}!</h1></body></html>'

        # Si no se ha recibido el código de autorización, se devuelve un error
    return 'Authorization code not found.'


class FlaskConfig:
    '''Configuración de Flask'''
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    SECRET_KEY = 'la_asignatura_de_giw'  # Imprescindible para usar sesiones
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run()
