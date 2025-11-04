from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.lista_productos, name='lista'),
    path('nuevo/', views.crear_producto, name='crear'),
    path('<int:pk>/editar/', views.editar_producto, name='editar'),
    path('<int:pk>/', views.detalle_producto, name='detalle'),
    path('eliminar/<int:pk>/', views.eliminar_view, name='eliminar'),

]
