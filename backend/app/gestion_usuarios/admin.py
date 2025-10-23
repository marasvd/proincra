# gestion_usuarios/admin.py
from django.contrib import admin
from .models import Rol, Actor, RolModuloPermisos

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreModulo', 'descripcion')
    search_fields = ('nombreModulo',)

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'tipoActor', 'rol', 'email')
    list_filter = ('tipoActor', 'rol')
    search_fields = ('username', 'documento', 'email')

@admin.register(RolModuloPermisos)
class RolModuloPermisosAdmin(admin.ModelAdmin):
    list_display = ('rol', 'modulo', 'to_letters')
    list_filter = ('modulo', 'rol')
    search_fields = ('rol__nombreModulo',)
    readonly_fields = ()
