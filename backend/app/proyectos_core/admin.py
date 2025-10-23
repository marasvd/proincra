# proyectos_core/admin.py
from django.contrib import admin
from .models import Beneficiario, Avance

@admin.register(Beneficiario)
class BeneficiarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_beneficiario', 'documento', 'telefono', 'fecha_registro')
    search_fields = ('nombre_beneficiario', 'documento')

@admin.register(Avance)
class AvanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'gestion', 'estado', 'fecha_avance')
    list_filter = ('estado',)
    search_fields = ('gestion__documento', 'gestion__nombre_beneficiario')
