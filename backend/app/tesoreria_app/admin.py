
from django.contrib import admin
from .models import OrdenPago

@admin.register(OrdenPago)
class OrdenPagoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'proveedor', 'monto', 'estado', 'fecha_emision', 'fecha_pago')
    list_filter = ('estado',)
    search_fields = ('numero', 'proveedor')

# Register your models here.
