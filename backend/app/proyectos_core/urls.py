# proyectos_core/urls.py
from django.urls import path
from . import views

app_name = 'proyectos_core'

urlpatterns = [
    path('', views.lista_avances, name='lista'),
    path('nuevo/', views.crear_avance, name='crear'),
    path('<int:id>/', views.detalle_avance, name='detalle'),
]
