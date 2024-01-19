from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Opinion(models.Model):
    """Modelo para almacenar la opinion de un usuario"""
    # Identificador único autogenerado
    ident = models.BigAutoField(primary_key=True)
    
    # Puntuación entre 0 y 10
    puntuacion = models.SmallIntegerField(validators=[MinValueValidator(0), 
                                                      MaxValueValidator(10)])

    # Texto de máximo 200 caracteres
    texto = models.CharField(max_length=200)

    # Al crear una opinion se pone la fecha actual
    fecha = models.DateTimeField(auto_now_add=True)

    # Referencia a un usuario del sistema. Si se elimina el usuario, este campo se pone a NULL
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    def clean(self):
        if self.puntuacion < 5 and len(self.texto.split()) < 5:
            raise ValidationError("Puntuacion negativa poco motivada")
        

    def __str__(self):
        """Para mostrar detalles en la interfaz admin"""
        return f"Opinión({self.puntuacion}, {self.texto}, {self.autor})"
