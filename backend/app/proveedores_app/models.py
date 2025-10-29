from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=20, unique=True)
    contacto = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    direccion = models.CharField(max_length=150)
    tipo_producto = models.CharField(max_length=100)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.nit}"

