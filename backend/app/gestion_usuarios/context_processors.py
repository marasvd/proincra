# app/gestion_usuarios/context_processors.py
from .models import Modulo

def modulos_disponibles(request):
    """
    Inyecta en el contexto de todas las plantillas una lista de módulos
    a los que el usuario actual tiene acceso (permiso 'V').
    Si el usuario no está autenticado, devuelve una lista vacía.
    """
    if not request.user.is_authenticated:
        return {'modulos_disponibles': []}

    actor = request.user
    modulos = []

    for modulo_key, modulo_name in Modulo.choices:
        if actor.has_perm_module(modulo_key, 'V'):
            modulos.append({
                'codigo': modulo_key,
                'nombre': modulo_name
            })

    return {'modulos_disponibles': modulos}
