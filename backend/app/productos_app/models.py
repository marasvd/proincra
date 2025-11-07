from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=50, choices=[
        ('material', 'Material'),
        ('herramienta', 'Herramienta'),
        ('equipamiento', 'Equipamiento'),
    ])
    unidad = models.CharField(max_length=50, default='Unidad')
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    actualizado_en = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.nombre} ({self.categoria})"
