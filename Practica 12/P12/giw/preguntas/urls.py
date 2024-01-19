from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'preguntas'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', login_required(views.logout_view), name='logout'),
    path('<int:question_id>/', login_required(views.pregunta), name='pregunta'),
    path('<int:question_id>/respuesta/', login_required(views.respuesta), name='respuesta'),
]
