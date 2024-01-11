# Definición de los urls dentro de la app

from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    # Índice
    path('index', views.index, name='index'),

    # Buscar producto según el buscador
    path('buscar-producto/',
         views.buscar_producto, name='buscar_producto'),

    # Buscar categoría según la barra de navegación
    path('buscar-categoria/<str:categoria>/',
         views.buscar_categoria, name='buscar_categoria'),

    # Formulario de nuevo producto
    path('nuevo-producto', views.nuevo_producto, name='nuevo_producto'),

    # Login
    path("", TemplateView.as_view(template_name="home.html"), name="home"),

]
