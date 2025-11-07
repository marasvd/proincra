from django.contrib import admin
from .models import EntradaInventario, SalidaInventario


# Registramos solo los modelos que realmente existen
@admin.register(EntradaInventario)
class EntradaInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'proveedor', 'fecha', 'responsable')
    search_fields = ('producto__nombre', 'proveedor__nombre')
    list_filter = ('fecha', 'proveedor')


@admin.register(SalidaInventario)
class SalidaInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'destino', 'fecha', 'responsable')
    search_fields = ('producto__nombre', 'destino')
    list_filter = ('fecha',)
