from django.contrib import admin

# Register your models here.

# Mostrar las opiniones en la interfaz de administración (ver, crear, editar, borrar)
from .models import Opinion
admin.site.register(Opinion)
