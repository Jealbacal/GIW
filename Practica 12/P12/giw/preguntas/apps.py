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
from django.apps import AppConfig


class PreguntasConfig(AppConfig):
    '''Clase PreguntasConfig'''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'preguntas'
