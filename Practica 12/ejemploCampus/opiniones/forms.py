from django import forms


class LoginForm(forms.Form):
    """Formulario para autenticar usuarios"""
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput)


class OpinionForm(forms.Form):
    """Formulario para añadir opiniones"""
    puntuacion = forms.IntegerField(min_value=0, max_value=10, required=True, label="Tu puntuación")
    texto = forms.CharField(max_length=200, label='Tu comentario')
    
    def clean_texto(self):
        """Limpieza personalizada: texto en minúsculas"""
        return self.cleaned_data['texto'].lower()
