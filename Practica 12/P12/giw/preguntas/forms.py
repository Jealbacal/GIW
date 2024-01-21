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
from django import forms

class LoginForm(forms.Form):
    '''Login form'''
    username = forms.CharField(label="Nombre de usuario", max_length=64)
    password = forms.CharField(label="Contraseña", max_length=64, widget=forms.PasswordInput)

class PreguntaForm(forms.Form):
    '''Pregunta form'''
    titulo = forms.CharField(label="Titulo", max_length=250)
    texto = forms.CharField(label="Pregunta", max_length=5000, widget=forms.Textarea)

class RespuestaForm(forms.Form):
    '''Respuesta form'''
    texto = forms.CharField(label="Respuesta", max_length=5000, widget=forms.Textarea)
