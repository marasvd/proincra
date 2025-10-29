from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.lista_proveedores, name='lista'),
    path('nuevo/', views.crear_proveedor, name='crear'),
    path('<int:id>/', views.detalle_proveedor, name='detalle'),
    path('<int:id>/editar/', views.editar_proveedor, name='editar'),
    path('<int:id>/eliminar/', views.eliminar_proveedor, name='eliminar'),
]
