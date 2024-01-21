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
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.
class Pregunta(models.Model):
    '''Definicion de la clase pregunta'''
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=250)
    texto = models.TextField(max_length=5000)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def num_respuestas(self):
        '''Funcion auxiliar que devuelve el numero de respuestas de la pregunta'''
        return Respuesta.objects.filter(pregunta=self).count()

    def clean(self):
        '''Validacion de la clase pregunta'''
        if self.titulo == self.texto: # Comprueba que el título y el texto no sean iguales
            raise ValidationError("El título y el texto no pueden ser iguales")

    def __str__(self):
        return f"Pregunta({self.titulo}, {self.texto}, {self.fecha_publicacion}, {self.autor})"


class Respuesta(models.Model):
    '''Definicion de la clase Respuesta'''
    id = models.BigAutoField(primary_key=True)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.TextField(max_length=5000)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"Respuesta({self.pregunta}, {self.texto}, {self.fecha_publicacion}, {self.autor})"
    