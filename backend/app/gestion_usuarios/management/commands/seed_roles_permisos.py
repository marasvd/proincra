from django.core.management.base import BaseCommand
from app.gestion_usuarios.models import Rol, RolModuloPermisos, Modulo

class Command(BaseCommand):
    help = "Crea roles y permisos iniciales en base a la matriz definida."

    def handle(self, *args, **options):
        ROLES_PERM_MATRIX = {
            "Administrador": {
                Modulo.BENEFICIARIOS: "VE",
                Modulo.INVENTARIO: "V",
                Modulo.PROYECTOS: "V",
                Modulo.CONTABILIDAD: "V",
                Modulo.AUDITORIA: "VX",
                Modulo.CONTRATACION: "V",
                Modulo.FACTURACION: "V",
                Modulo.PROVEEDORES: "V",
                Modulo.USUARIOS: "VU",
                Modulo.CARTERA: "V",
                Modulo.NOMINA: "V",
                Modulo.COMPRAS: "V",
                Modulo.OPERACIONES_TI: "VU",
                Modulo.TESORERIA: "V", 
            },
            "Almacenista": {
                Modulo.BENEFICIARIOS: "V",
                Modulo.INVENTARIO: "VCED",
                Modulo.PROYECTOS: "V",
                Modulo.CONTABILIDAD: "V",
                Modulo.AUDITORIA: "V",
                Modulo.CONTRATACION: "V",
                Modulo.FACTURACION: "V",
                Modulo.PROVEEDORES: "V",
                Modulo.USUARIOS: "V",
                Modulo.CARTERA: "V",
                Modulo.NOMINA: "V",
                Modulo.COMPRAS: "CR",
                Modulo.OPERACIONES_TI: "V",
            },
            "Técnico de Campo": {
                Modulo.BENEFICIARIOS: "CV",
                Modulo.INVENTARIO: "V",
                Modulo.PROYECTOS: "CES",
                Modulo.CONTABILIDAD: "V",
                Modulo.AUDITORIA: "V",
                Modulo.CONTRATACION: "V",
                Modulo.FACTURACION: "V",
                Modulo.PROVEEDORES: "V",
                Modulo.USUARIOS: "V",
                Modulo.CARTERA: "V",
                Modulo.NOMINA: "V",
                Modulo.COMPRAS: "R",
                Modulo.OPERACIONES_TI: "S",
            },
            "Contabilidad / Tesorería": {
                Modulo.CONTABILIDAD: "VCPX",
                Modulo.TESORERIA: "VCPX",  # <- y también aquí, este es su módulo natural
                Modulo.CARTERA: "V",
                Modulo.FACTURACION: "R",
                Modulo.NOMINA: "P",
            },
        }

        for nombre_rol, modulos in ROLES_PERM_MATRIX.items():
            rol, created = Rol.objects.get_or_create(nombreModulo=nombre_rol)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Rol creado: {nombre_rol}"))
            else:
                self.stdout.write(self.style.WARNING(f"Rol ya existía: {nombre_rol}"))

            for modulo, permisos in modulos.items():
                rol.set_perm_for_module(modulo, permisos)

        self.stdout.write(self.style.SUCCESS("Roles y permisos cargados correctamente."))
