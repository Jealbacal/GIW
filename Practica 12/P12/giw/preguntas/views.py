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
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods
from .models import Pregunta, Respuesta
from .forms import LoginForm, PreguntaForm, RespuestaForm


# Create your views here.

def index(request):
    """Muestra todas las preguntas"""
    preguntas = Pregunta.objects.order_by('-fecha_publicacion')
    return render(request, "preguntas.html", {'preguntas': preguntas})

@require_http_methods(["GET", "POST"])
def loginfunct(request):
    """Muestra el formulario (GET) o recibe los datos y realiza la autenticacion (POST)"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {'login_form': form})

    form = LoginForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

    # Toma los datos limpios del formulario
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    # Realiza la autenticación
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)  # Registra el usuario en la sesión
        return redirect(reverse('preguntas:index')) #redirigir a la pagina principal

    return HttpResponseBadRequest("Usuario o contraseña incorrectos")

@require_GET
def logoutfunct(request):
    """Elimina al usuario de la sesión actual"""
    logout(request)  # Elimina el usuario de la sesión
    return redirect(reverse('preguntas:index'))


@require_http_methods(["GET", "POST"])
def preguntas(request):
    """Muestra todas las preguntas (GET) o recibe el formulario y añade la pregunta (POST)"""
    if request.method == "POST":
        form = PreguntaForm(request.POST)
        if form.is_valid():
            pregunta = Pregunta(titulo=form.cleaned_data['titulo'],
                                texto=form.cleaned_data['texto'],
                                autor=request.user
            ) # Crea el objeto pregunta
            pregunta.save() # Guarda el objeto en la base de datos
            return redirect(reverse('preguntas:index'))

        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")
    # GET
    todas_preguntas = Pregunta.objects.order_by('-fecha_publicacion')
    form = PreguntaForm() if request.user.is_authenticated else None

    return render(request, "preguntas.html", {'preguntas': todas_preguntas, 'form': form})

@require_http_methods(["GET", "POST"])
@login_required(login_url='/preguntas/login/')# si no esta logueado, redirige a la pagina de login
def pregunta(request, question_id): # question_id es el id de la pregunta
    """Muestra la pregunta (GET)"""
    if request.method == "POST":
        form = RespuestaForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")
        respuesta = Respuesta()
        respuesta.texto = form.cleaned_data['texto']
        respuesta.autor = request.user
        respuesta.pregunta = Pregunta.objects.get(id=question_id)
        respuesta.save()
        return redirect(reverse('preguntas:pregunta', args=(question_id,)))

    pregunta = Pregunta.objects.get(id=question_id) # obtiene la pregunta con el id
    respuestas = Respuesta.objects.filter(pregunta=pregunta).order_by('-fecha_publicacion')
    form = RespuestaForm()
    return render(request, "preguntas_detalles.html", \
                    {'pregunta_datos': pregunta, 'respuestas': respuestas, 'form': form})
