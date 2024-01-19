from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator , MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Pregunta(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=250)
    texto = models.TextField(max_length=5000)
    fecha_publicacion = models.DateTimeField('fecha de publicacion')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"Pregunta({self.titulo}, {self.texto}, {self.fecha_publicacion}, {self.autor})"
    
class Usuario(models.Model):
    nombre = models.CharField(max_length=200, primary_key=True)
    password = models.CharField(max_length=512)
    def __str__(self):
        return f"Usuario({self.nombre}, {self.password})"
    
class Respuesta(models.Model):
    id = models.BigAutoField(primary_key=True)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.TextField(max_length=5000)
    fecha_publicacion = models.DateTimeField('fecha de publicacion')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"Respuesta({self.pregunta}, {self.texto}, {self.fecha_publicacion}, {self.autor})"