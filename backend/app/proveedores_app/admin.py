from django.contrib import admin
from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'contacto', 'telefono', 'tipo_producto', 'fecha_registro')
    search_fields = ('nombre', 'nit')
