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
from django.contrib import admin
from django.urls import path, include
from app.gestion_usuarios import views_auth
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),

    # Módulos del backend (apps Django)
    path('beneficiarios/', include(('app.proyectos_core.urls', 'proyectos_core'), namespace='proyectos_core')),
    path('usuarios/', include(('app.gestion_usuarios.urls_auth', 'gestion_usuarios'), namespace='gestion_usuarios')),

    # Frontend global (páginas generales)
    path('', views_auth.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', views_auth.dashboard_view, name='dashboard'),
]
