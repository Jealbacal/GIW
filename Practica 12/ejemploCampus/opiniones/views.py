from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods
from django.core.exceptions import ValidationError

from .forms import LoginForm, OpinionForm
from .models import Opinion


@require_GET
def index(request):
    opiniones = Opinion.objects.order_by('-fecha')
    return render(request, "opiniones.html", {'opiniones': opiniones})


@require_http_methods(["GET", "POST"])
def loginfunct(request):
    """Muestra el formulario (GET) o recibe los datos y realiza la autenticacion (POST)"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {'login_form': form})

    # Carga el formulario desde los datos de la petición y lo valida
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
        return redirect(reverse('opiniones:index'))
    else:
        return HttpResponseBadRequest("Usuario o contraseña incorrectos")


@require_GET
def logoutfunct(request):
    """Elimina al usuario de la sesión actual"""
    logout(request)  # Elimina el usuario de la sesión
    return redirect(reverse('opiniones:index'))


@login_required(login_url='opiniones:login')
@require_http_methods(["GET", "POST"])
def nueva_opinion(request):
    """Muestra el formulario de nueva opinión (GET) o recibe el formulario y añade la opinión (POST)"""
    if request.method == "GET":
        form = OpinionForm()
        return render(request, "nueva_opinion.html", {'opinion_form': form})

    form = OpinionForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")
    punt_f = form.cleaned_data['puntuacion']
    texto_f = form.cleaned_data['texto']

    # Crea un objeto ORM a partir de los datos limpios del formulario y lo salva en la BD
    opinion = Opinion(puntuacion=punt_f, texto=texto_f, autor=request.user)
    try:
        opinion.full_clean()
        opinion.save()
    except ValidationError as e:
        return HttpResponseBadRequest("Opinión mal formada")

    return redirect(reverse('opiniones:index'))
