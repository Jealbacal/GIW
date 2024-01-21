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
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'preguntas'

urlpatterns = [
    path('', views.preguntas, name='index'),
    path('login/', views.loginfunct, name='login'),
    path('logout/', login_required(views.logoutfunct), name='logout'),
    path('<int:question_id>/', login_required(views.pregunta), name='pregunta'),
    #path('<int:question_id>/respuesta/', login_required(views.respuesta), name='respuesta'),
]
