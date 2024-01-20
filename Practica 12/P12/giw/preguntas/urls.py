from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'preguntas'

urlpatterns = [
    path('', views.preguntas, name='index'),
    path('login/', views.loginfunct, name='login'),
    path('logout/', login_required(views.logoutfunct), name='logout'),
    path('<int:question_id>/', login_required(views.pregunta), name='pregunta'),
    #path('<int:question_id>/respuesta/', login_required(views.respuesta), name='respuesta'),
]
