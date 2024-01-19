from django.urls import path

from . import views

# Imprescindible dar un nombre para crear un namespace y poder referirse a estas rutas como
# opiniones:index, opiniones:login, etc.
app_name = "opiniones"

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginfunct, name='login'),
    path('logout', views.logoutfunct, name='logout'),
    path('nueva_opinion', views.nueva_opinion, name='nueva_opinion'),
]
