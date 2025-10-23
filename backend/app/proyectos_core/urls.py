# proyectos_core/urls.py
from django.urls import path
from . import views

app_name = 'proyectos_core'

urlpatterns = [
    path('', views.BeneficiarioListView.as_view(), name='beneficiario_list'),
    path('nuevo/', views.BeneficiarioCreateView.as_view(), name='beneficiario_create'),
    path('<int:pk>/', views.BeneficiarioDetailView.as_view(), name='beneficiario_detail'),
    path('<int:pk>/editar/', views.BeneficiarioUpdateView.as_view(), name='beneficiario_update'),
    path('<int:pk>/eliminar/', views.BeneficiarioDeleteView.as_view(), name='beneficiario_delete'),
]
