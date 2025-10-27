# proyectos_core/admin.py
from django.contrib import admin
from .models import AvanceProyecto, Evidencia  # ← Importa los modelos correctos

@admin.register(AvanceProyecto)
class AvanceProyectoAdmin(admin.ModelAdmin):
    list_display = ('id', 'beneficiario', 'tecnico', 'porcentaje_avance', 'estado', 'fecha')
    search_fields = ('beneficiario__nombre', 'tecnico__username')
    list_filter = ('estado', 'fecha')
    ordering = ('-fecha',)

@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'avance', 'fecha_subida')
    search_fields = ('avance__beneficiario__nombre',)
