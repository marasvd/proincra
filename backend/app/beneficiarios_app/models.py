from django.db import models

class Beneficiario(models.Model):
    ESTADOS = [
        ('terminado', 'Terminado'),
        ('en_construccion', 'En construcción'),
        ('pendiente', 'Pendiente'),
    ]

    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"
