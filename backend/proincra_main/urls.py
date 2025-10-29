"""
URL configuration for proincra_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# proincra_main/urls.py
# proincra_main/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    # -------------------------------------------
    # PÁGINA PÚBLICA (inicio general del sistema)
    # -------------------------------------------
    path('', TemplateView.as_view(template_name='public/index.html'), name='home'),

    # -------------------------------------------
    # ADMINISTRACIÓN DE DJANGO
    # -------------------------------------------
    path('admin/', admin.site.urls),

    # -------------------------------------------
    # MÓDULOS DEL BACKEND (apps Django)
    # -------------------------------------------
    path('proyectos/', include(('app.proyectos_core.urls', 'proyectos_core'), namespace='proyectos_core')),
    path('usuarios/', include(('app.gestion_usuarios.urls_auth', 'gestion_usuarios'), namespace='gestion_usuarios')),
    path('beneficiarios/', include(('app.beneficiarios_app.urls', 'beneficiarios_app'), namespace='beneficiarios')),
    path('inventario/', include(('app.inventario_app.urls', 'inventario'), namespace='inventario')),
    path('proveedores/', include(('app.proveedores_app.urls', 'proveedores_app'), namespace='proveedores_app')),

    # -------------------------------------------
    # OPCIONAL: redirección raíz → login
    # (Descomenta si quieres que "/" redirija al login)
    # -------------------------------------------
    # path('', RedirectView.as_view(pattern_name='gestion_usuarios:login', permanent=False)),
]
