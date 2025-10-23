# proyectos_core/models.py
from django.db import models

class Beneficiario(models.Model):
    nombre_beneficiario = models.CharField(max_length=255)
    documento = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Beneficiario"
        verbose_name_plural = "Beneficiarios"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre_beneficiario} — {self.documento}"


class Avance(models.Model):
    gestion = models.ForeignKey(
        Beneficiario,
        on_delete=models.CASCADE,
        related_name='avances',
        db_column='gestion_id',
        verbose_name='Beneficiario (gestion_id)'
    )
    descripcion = models.TextField()
    estado = models.CharField(max_length=100)  # considera usar Choices en producción
    fecha_avance = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avance"
        verbose_name_plural = "Avances"
        ordering = ['-fecha_avance']

    def __str__(self):
        return f"Avance {self.pk} — {self.gestion.documento} — {self.estado}"
