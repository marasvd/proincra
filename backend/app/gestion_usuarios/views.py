from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.gestion_usuarios.models import Actor
from app.gestion_usuarios.models import RolModuloPermisos

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
    modulos_permitidos = []

    if hasattr(user, 'rol'):
        permisos = RolModuloPermisos.objects.filter(rol=user.rol)
        for p in permisos:
            if 'V' in p.permisos:
                modulos_permitidos.append((p.modulo, p.permisos))

        # Limpiar duplicados y vacíos
    modulos_permitidos = [
        (m, p) for m, p in modulos_permitidos 
        if m and str(m).strip() and hasattr(m, '__str__')
    ]

    # Asegurar que 'm' no sea None ni cadena vacía
    modulos_permitidos = [(str(m).strip(), p) for m, p in modulos_permitidos if str(m).strip()]

    # Eliminar duplicados conservando orden
    vistos = set()
    modulos_permitidos = [(m, p) for m, p in modulos_permitidos if not (m in vistos or vistos.add(m))]

    return render(request, 'dashboard/dashboard.html', {
        'modulos': modulos_permitidos,
        'user': user,
    })


def signup_view(request):
    return render(request, 'auth/signup.html')
