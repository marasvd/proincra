from django.db import models
from django.db import models
from django.utils import timezone

class OrdenPago(models.Model):
    numero = models.CharField(max_length=50, unique=True)
    proveedor = models.CharField(max_length=150)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_emision = models.DateTimeField(default=timezone.now)
    fecha_pago = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('pagado', 'Pagado'),
            ('rechazado', 'Rechazado'),
        ],
        default='pendiente'
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Orden de Pago"
        verbose_name_plural = "Órdenes de Pago"
        ordering = ['-fecha_emision']

    def __str__(self):
        return f"Orden #{self.numero} - {self.proveedor}"

# Create your models here.
