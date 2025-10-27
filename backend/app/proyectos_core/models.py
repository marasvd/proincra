# backend/app/proyectos_core/models.py
from django.db import models
from app.beneficiarios_app.models import Beneficiario
from django.conf import settings



class AvanceProyecto(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('finalizado', 'Finalizado'),
    ]

    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE, related_name='avances')
    tecnico = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='avances_registrados'
)

    fecha = models.DateField(auto_now_add=True)
    porcentaje_avance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"Avance {self.id} - {self.beneficiario.nombre}"
class Evidencia(models.Model):
    avance = models.ForeignKey(AvanceProyecto, on_delete=models.CASCADE, related_name='evidencias')
    imagen = models.ImageField(upload_to='evidencias/', blank=True, null=True)
    coordenadas_gps = models.CharField(max_length=100, blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evidencia {self.id} del avance {self.avance.id}"
