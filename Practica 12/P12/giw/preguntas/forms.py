from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=64)
    password = forms.CharField(label="Contraseña", max_length=64, widget=forms.PasswordInput)

class PreguntaForm(forms.Form):
    titulo = forms.CharField(label="Titulo", max_length=250)
    texto = forms.CharField(label="Pregunta", max_length=5000, widget=forms.Textarea)

class RespuestaForm(forms.Form):
    texto = forms.CharField(label="Respuesta", max_length=5000, widget=forms.Textarea)
