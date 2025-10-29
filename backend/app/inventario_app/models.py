# backend/app/inventario_app/models.py
from decimal import Decimal
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from app.proveedores_app.models import Proveedor


class Categoria(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    UNIDADES = (
        ('UN', 'Unidad'),
        ('KG', 'Kilogramo'),
        ('LT', 'Litro'),
        ('MT', 'Metro'),
    )

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    unidad_medida = models.CharField(max_length=2, choices=UNIDADES, default='UN')
    stock = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0'))
    stock_minimo = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0'))
    precio_unitario = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0'))
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('nombre', 'categoria'),)
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_unidad_medida_display()})"

    @property
    def valor_total(self):
        return self.stock * self.precio_unitario

    @property
    def en_bajo_stock(self):
        return self.stock <= self.stock_minimo


class MovimientoBase(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="%(class)ss")
    cantidad = models.DecimalField(max_digits=14, decimal_places=2)
    observaciones = models.TextField(blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="%(class)ss")

    class Meta:
        abstract = True
        ordering = ['-fecha']


class EntradaInventario(MovimientoBase):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='entradas')

    class Meta:
        verbose_name = "Entrada de inventario"
        verbose_name_plural = "Entradas de inventario"

    def aplicar(self):
        self.producto.stock = (self.producto.stock or 0) + self.cantidad
        self.producto.save(update_fields=['stock', 'actualizado_en'])

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        with transaction.atomic():
            super().save(*args, **kwargs)
            if is_new:
                self.aplicar()


class SalidaInventario(MovimientoBase):
    destino = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Salida de inventario"
        verbose_name_plural = "Salidas de inventario"

    def aplicar(self):
        nuevo_stock = (self.producto.stock or 0) - self.cantidad
        if nuevo_stock < 0:
            raise ValueError("No hay stock suficiente para esta salida.")
        self.producto.stock = nuevo_stock
        self.producto.save(update_fields=['stock', 'actualizado_en'])

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        with transaction.atomic():
            super().save(*args, **kwargs)
            if is_new:
                self.aplicar()
