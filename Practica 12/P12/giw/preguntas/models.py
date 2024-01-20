from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.
class Pregunta(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=250)
    texto = models.TextField(max_length=5000)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def num_respuestas(self): # Devuelve el número de respuestas de la pregunta
        return Respuesta.objects.filter(pregunta=self).count()

    def clean(self):
        if self.titulo == self.texto: # Comprueba que el título y el texto no sean iguales
            raise ValidationError("El título y el texto no pueden ser iguales")

    def __str__(self):
        return f"Pregunta({self.titulo}, {self.texto}, {self.fecha_publicacion}, {self.autor})"


class Respuesta(models.Model):
    id = models.BigAutoField(primary_key=True)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.TextField(max_length=5000)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"Respuesta({self.pregunta}, {self.texto}, {self.fecha_publicacion}, {self.autor})"