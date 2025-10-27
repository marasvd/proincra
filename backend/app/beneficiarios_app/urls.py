from django.urls import path
from . import views

app_name = 'beneficiarios'

urlpatterns = [
    path('', views.lista_beneficiarios, name='lista'),
    path('nuevo/', views.crear_beneficiario, name='crear'),
    path('<int:id>/', views.detalle_beneficiario, name='detalle'),
]
