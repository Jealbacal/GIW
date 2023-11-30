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
import json
from flask import Flask, request, session, render_template,jsonify
app = Flask(__name__)


###
### <DEFINIR AQUI EL SERVICIO REST>
###

def esvalido(asig):
    return "nombre" in asig and "numero_alumnos" in asig and "horario" in asig\
            and isinstance(asig["nombre"],str) and isinstance(asig["numero_alumnos"],int)\
            and isinstance(asig["horario"],list)



@app.route('/asignaturas',methods=['POST'])
def añadeAsig():

    try :
        asig = request.get_data(as_text=True)
        json_data = json.loads(asig)
        #asig["id"] = len(asig)
        # # if not esvalido(asig):
        # #     return jsonify({"error": "error asignatura"}),400
        
        #return jsonify({"id":asig["id"]}),201
        return jsonify(json_data)

    except Exception as ex:

        return jsonify({"error":str(ex)}),400
        
    

@app.route('/asignaturas',methods=['DEL'])
def eliminarAsig():
    ...

@app.route('/asignaturas',methods=['DEL'])
def verAsig():
    ...


class FlaskConfig:
    """Configuración de Flask"""
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = "giw_clave_secreta"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run(host="localhost",port=5000,debug= True)

