# gestion_usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.Model):
    nombreModulo = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombreModulo

    def set_perm_for_module(self, modulo, perm_letters: str):
        """Crea/actualiza RolModuloPermisos según una cadena de letras tipo 'VCE'."""
        rmp, _ = RolModuloPermisos.objects.get_or_create(rol=self, modulo=modulo)
        rmp.set_from_letters(perm_letters)
        rmp.save()


class Actor(AbstractUser):
    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name='actores',
        db_column='rolModulo_id',
        verbose_name='Rol / Módulo ',
        null=True,     
        blank=True
        )

    class TipoActorChoices(models.TextChoices):
        ALMACENISTA = 'ALMACENISTA', 'Almacenista'
        TECNICO_CAMPO = 'TECNICO_CAMPO', 'Técnico Campo'
        BENEFICIARIO = 'BENEFICIARIO', 'Beneficiario'
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
        SUPERVISOR = 'SUPERVISOR', 'Supervisor'
        CONTRATISTA = 'CONTRATISTA', 'Contratista'
        PROVEEDOR = 'PROVEEDOR', 'Proveedor'
        CONTADOR = 'CONTADOR', 'Contabilidad'
        FACTURADOR = 'FACTURADOR', 'Facturación'
        RRHH = 'RRHH', 'Recursos Humanos'
        OPER_TIC = 'OPER_TIC', 'Operaciones TI'

    tipoActor = models.CharField(
        max_length=30,
        choices=TipoActorChoices.choices,
        default=TipoActorChoices.ADMINISTRADOR
    )

    telefono = models.CharField(max_length=30, blank=True, null=True)
    documento = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Actor (Usuario)"
        verbose_name_plural = "Actores (Usuarios)"

    def __str__(self):
        return f"{self.username} ({self.get_tipoActor_display()})"

    def has_perm_module(self, modulo: str, letter: str) -> bool:
        """
        Comprueba si el actor (según su rol) tiene el permiso indicado (letra) en el modulo.
        letter: una de 'V','C','E','D','A','R','P','S','U','X'
        """
        if not self.rol:
            return False
        try:
            rmp = RolModuloPermisos.objects.get(rol=self.rol, modulo=modulo)
        except RolModuloPermisos.DoesNotExist:
            return False

        letter = letter.upper()
        mapping = {
            'V': rmp.ver,
            'C': rmp.crear,
            'E': rmp.editar,
            'D': rmp.eliminar,
            'A': rmp.aprobar,
            'R': rmp.revisar,
            'P': rmp.procesar_pago,
            'S': rmp.sincronizar,
            'U': rmp.gestionar_usuarios,
            'X': rmp.exportar,
        }
        return mapping.get(letter, False)

    def get_modulos_permitidos(self):
        """
        Retorna lista de tuplas (modulo, permisos_str) que tiene el rol del usuario.
        permisos_str es una cadena con letras concatenadas, p.ej 'VCE'
        """
        permisos = []
        for rmp in self.rol.permisos_modulos.all():
            letters = rmp.to_letters()
            permisos.append((rmp.modulo, letters))
        return permisos


class Modulo(models.TextChoices):
    BENEFICIARIOS = 'beneficiarios', '1 Beneficiarios'
    INVENTARIO = 'inventario', '2 Inventario (Producción)'
    PROYECTOS = 'proyectos', '3 Proyectos / Avance'
    CONTABILIDAD = 'contabilidad', '4 Contabilidad'
    AUDITORIA = 'auditoria', '5 Auditoría'
    CONTRATACION = 'contratacion', '6 Contratación / Obra'
    FACTURACION = 'facturacion', '7 Facturación'
    PROVEEDORES = 'proveedores', '8 Proveedores'
    USUARIOS = 'usuarios', '9 Usuarios y Roles'
    CARTERA = 'cartera', '10 Cartera'
    NOMINA = 'nomina', '11 Nómina'
    COMPRAS = 'compras', '12 Compras'
    OPERACIONES_TI = 'operaciones_ti', '13 Operaciones TI / Docs'
    TESORERIA = 'tesoreria', '14 Tesorería'



class RolModuloPermisos(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='permisos_modulos')
    modulo = models.CharField(max_length=50, choices=Modulo.choices)
    ver = models.BooleanField(default=False)             # V
    crear = models.BooleanField(default=False)           # C
    editar = models.BooleanField(default=False)          # E
    eliminar = models.BooleanField(default=False)        # D
    aprobar = models.BooleanField(default=False)         # A
    revisar = models.BooleanField(default=False)         # R
    procesar_pago = models.BooleanField(default=False)   # P
    sincronizar = models.BooleanField(default=False)     # S
    gestionar_usuarios = models.BooleanField(default=False)  # U
    exportar = models.BooleanField(default=False)        # X

    class Meta:
        unique_together = ('rol', 'modulo')
        verbose_name = "Permisos por Rol y Módulo"
        verbose_name_plural = "Permisos por Roles y Módulos"

    def __str__(self):
        return f"{self.rol.nombreModulo} @ {self.get_modulo_display()}"

    def set_from_letters(self, letters: str):
        """
        Define los booleanos según una cadena de letras.
        """
        letters = letters.upper()
        self.ver = 'V' in letters
        self.crear = 'C' in letters
        self.editar = 'E' in letters
        self.eliminar = 'D' in letters
        self.aprobar = 'A' in letters
        self.revisar = 'R' in letters
        self.procesar_pago = 'P' in letters
        self.sincronizar = 'S' in letters
        self.gestionar_usuarios = 'U' in letters
        self.exportar = 'X' in letters

    def to_letters(self):
        letters = []
        if self.ver: letters.append('V')
        if self.crear: letters.append('C')
        if self.editar: letters.append('E')
        if self.eliminar: letters.append('D')
        if self.aprobar: letters.append('A')
        if self.revisar: letters.append('R')
        if self.procesar_pago: letters.append('P')
        if self.sincronizar: letters.append('S')
        if self.gestionar_usuarios: letters.append('U')
        if self.exportar: letters.append('X')
        return ''.join(letters)
