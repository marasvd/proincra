from django.contrib import admin
from .models import Categoria, Producto, EntradaInventario, SalidaInventario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'unidad_medida', 'stock', 'stock_minimo', 'precio_unitario', 'activo')
    list_filter = ('categoria', 'unidad_medida', 'activo')
    search_fields = ('nombre', 'descripcion')

@admin.register(EntradaInventario)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'responsable', 'fecha', 'proveedor')
    list_filter = ('fecha', 'responsable')
    search_fields = ('producto__nombre', 'proveedor', 'observaciones')

@admin.register(SalidaInventario)
class SalidaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'responsable', 'fecha', 'destino')
    list_filter = ('fecha', 'responsable')
    search_fields = ('producto__nombre', 'destino', 'observaciones')
