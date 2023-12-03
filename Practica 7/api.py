"""
Asignatura: GIW
Práctica 7
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

from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError

app = Flask(__name__)

class FlaskConfig:
    """Configuracion inical Flask"""
    ENV = 'development'
    DEBUG = True
    TEST = True
    SECRET_KEY = "giw_clave_secreta"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class Asignatura:
    """Estructura Asignatura"""
    def __init__(self, id, nombre, numero_alumnos, horario):
        self.id = id
        self.nombre = nombre
        self.numero_alumnos = numero_alumnos
        self.horario = horario

asignaturas_list = []
asignatura_id_counter = 0

esquema = { #Esquema para validar la estrucutura de los json
    "type": "object",
    "properties": {
        "nombre": {"type": "string"},
        "numero_alumnos": {"type": "integer"},
        "horario": {
            "type": ["array","null"],
            "items": {
                "type": "object",
                "properties": {
                    "dia": {"type": "string"},
                    "hora_inicio": {"type": "integer"},
                    "hora_final": {"type": "integer"}
                },
                "required": ["dia", "hora_inicio", "hora_final"]
            }
        }
    },
    "required": ["nombre", "numero_alumnos", "horario"],
    "additionalProperties": False
}


@app.route('/', methods=['GET'])
def root():
    """TEST Pag inicio"""
    return 'Soy la página principal'

@app.route('/asignaturas',methods=['DELETE'])
def delete_asignaturas():
    """Elimina todas las asignaturas"""
    global asignatura_id_counter
    asignaturas_list.clear()#limpia lista
    asignatura_id_counter=0#contador a 0
    return '',204


def esvalido(asig):#comprobacion de json en parametro
    """Comprueba si el json es valido"""
    try:
        validate(instance=asig, schema=esquema)
        return True
    except ValidationError:
        return False

@app.route('/asignaturas', methods=['POST'])
def create_asignatura():
    """Crea un asignatura y le asigna un id"""
    global asignatura_id_counter

    data = request.get_json()
    if esvalido(data) is False:
        return '',400 #bad request

    asignatura = Asignatura(#creacion de clase assignatura
        id=asignatura_id_counter,
        nombre=data["nombre"],
        numero_alumnos=data["numero_alumnos"],
        horario=data["horario"]
    )

    asignaturas_list.append(asignatura)#lista global
    asignatura_id_counter += 1#contador global

    return {"id":asignatura_id_counter-1}, 201



@app.route('/asignaturas', methods=['GET'])  #get /asignatura
def get_asignaturas():
    """Devuelve una lista de asignaturas en funcion de parametros"""
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)
    alumnos_gte=request.args.get('alumnos_gte',type=int) #argumentos
    asignaturas_data=[]#array para return con jsonify


    if not page and not per_page and not alumnos_gte:#ninguno existe devuelve todos
        for asig in asignaturas_list:
            asignaturas_data.append(f"/asignaturas/{asig.id}")

        return jsonify({'asignaturas': asignaturas_data}), 200 #default devuelve 200


    if alumnos_gte and page and per_page:#existen las tres
        cont = 0
        processed=0
        for asig in asignaturas_list:
            if asig.numero_alumnos >= alumnos_gte:
                processed+=1
                if processed>page*per_page:
                    break
                if processed>(page-1)*per_page:
                    asignaturas_data.append(f"/asignaturas/{asig.id}")
                    cont += 1

        if len(asignaturas_data) < len(asignaturas_list):
            return jsonify({'asignaturas': asignaturas_data}), 206
        return jsonify({'asignaturas': asignaturas_data}), 200

    if alumnos_gte is not None: #tras las comprobaciones anteriores solo esta este
        for asig in asignaturas_list:
            if asig.numero_alumnos >= alumnos_gte:
                asignaturas_data.append(f"/asignaturas/{asig.id}")

        if len(asignaturas_data) < len(asignaturas_list):
            return jsonify({'asignaturas': asignaturas_data}), 206
        return jsonify({'asignaturas': asignaturas_data}), 200


    if page and per_page: #existen solo estas dos
        cont = 0
        # Si se pasa de indexacion entendemos que se devuelve todas las asignaturas
        # if page*per_page>len(asignaturas_list):
        #     return '',404#esta fuera de index
        for asig in asignaturas_list[(page-1)*per_page:(page*per_page)]:
            asignaturas_data.append(f"/asignaturas/{asig.id}")
            cont += 1
            if cont > per_page:
                return jsonify({'asignaturas': asignaturas_data}), 206

        if len(asignaturas_data) < len(asignaturas_list):
            return jsonify({'asignaturas': asignaturas_data}), 206
        return jsonify({'asignaturas': asignaturas_data}), 200

    #bad request no cumple con page&per_page
    return '',400

@app.route('/asignaturas/<int:id>', methods=['DELETE'])
def del_asignaturas(id):
    """Borra un asignatura dado su id"""
    for asig in asignaturas_list:
        if asig.id == id:
            asignaturas_list.remove(asig)
            return '',204
    return '',404

@app.route('/asignaturas/<int:id>', methods=['GET'])
def datos_asig(id):
    """Obtiene un asignatura dado su id"""
    for asig in asignaturas_list:
        if asig.id == id:
            return jsonify({"horario": asig.horario,
                    "id": asig.id,
                    "nombre": asig.nombre,
                    "numero_alumnos": asig.numero_alumnos
                    }), 200

    return '',404

@app.route('/asignaturas/<int:id>', methods=['PUT'])
def reemplaza_asig(id):
    """Modifica un asignatura dado su id y todos los campos"""

    for asig in asignaturas_list:
        if asig.id == id:

            data = request.get_json()
            if esvalido(data) is False:
                return '',400 #bad request

            asig.nombre = data["nombre"]
            asig.numero_alumnos=data["numero_alumnos"]
            asig.horario = data["horario"]

            return '',200 #ok

    return '', 404 #not found

def comprobar_horario(lista):
    """Comprueba que el json del horario sea valido"""
    for a in lista:
        if not isinstance(a,dict):
            return False
        if not len(a) == 0:
            # ----- Claves en dicc y tipo de datos de los valores -----
            if not ("dia" in a and "hora_inicio" in a and "hora_final" in a\
                and isinstance(a["dia"],str) and isinstance(a["hora_inicio"],int)\
                and isinstance(a["hora_final"],int) and (len(a) == 3)):
                return False

        else:
            return False

    return True


@app.route('/asignaturas/<int:id>', methods=['PATCH'])
def actualiza_asig(id):
    """Modifica un asignatura dado su id y un solo campo"""
    for asig in asignaturas_list:
        if asig.id == id:

            data = request.get_json()
            if len(data) != 1: #Diccionario de un solo campo
                return '',400
            key = list(data.keys()).pop() # La clave
            if key not in ["nombre" , "numero_alumnos", "horario"]:
                return '',400 #bad request

            if (key == "nombre") and isinstance(data[key],str):
                asig.nombre = data["nombre"]
                return '',200 #ok
            if (key == "numero_alumnos") and isinstance(data[key],int):
                asig.numero_alumnos = data["numero_alumnos"]
                return '',200 #ok
            if (key == "horario") and isinstance(data[key],list) and comprobar_horario(data[key]):
                asig.horario = data["horario"]
                return '',200 #ok

    return '',404

@app.route('/asignaturas/<int:id>/horario',methods=['GET'])
def gethorarios(id):
    """Devuelve el horario de la asignatura id"""
    for asig in asignaturas_list:
        if asig.id == id:
            return {"horario": asig.horario}, 200

    return '',404


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run(host="localhost", port=5000, debug=True)
