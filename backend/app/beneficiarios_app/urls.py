from django.urls import path
from . import views

app_name = 'beneficiarios'

urlpatterns = [
    path('', views.lista_beneficiarios, name='lista'),
    path('nuevo/', views.crear_beneficiario, name='crear'),
    path('<int:id>/', views.detalle_beneficiario, name='detalle'),
    path('dashboard/', views.dashboard_principal, name='dashboard'),
    path('eliminar/<int:pk>/', views.eliminar_beneficiario, name='eliminar_beneficiario'),
    path('<int:pk>/editar/', views.editar_beneficiario, name='editar_beneficiario'),
]
