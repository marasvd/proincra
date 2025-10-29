from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.lista_view, name='lista'),                 # Gestión general + filtros
    path('entrada/', views.entrada_view, name='entrada'),     # Registrar entrada
    path('salida/', views.salida_view, name='salida'),        # Registrar salida
    path('resumen/', views.resumen_view, name='resumen'),     # Resumen de inventario
    path('<int:pk>/', views.detalle_producto_view, name='detalle'),  # Detalle producto
]
