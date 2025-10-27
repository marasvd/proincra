from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.gestion_usuarios.models import Actor

# --- Vistas de autenticación ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('gestion_usuarios:dashboard')  # ← con namespace correcto
        else:
            return render(request, 'auth/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('gestion_usuarios:login')  # ← también corregido con namespace


@login_required
def dashboard_view(request):
    user = request.user
    modulos_permitidos = user.get_modulos_permitidos() if hasattr(user, 'rol') else []
    return render(
        request,
        'dashboard/dashboard.html',
        {'modulos': modulos_permitidos, 'user': user}
    )


def signup_view(request):
    return render(request, 'auth/signup.html')
