from django.core.management.base import BaseCommand
from core.models import Usuarios  # Ajusta si el modelo está en otro lugar

class Command(BaseCommand):
    help = "Crear usuarios iniciales con RUT y contraseña hasheada"

    def handle(self, *args, **kwargs):
        users_data = [
            {"rut": "12345678-9", "password": "admin123", "is_active": True, "rol": "admin"},
            {"rut": "98765432-1", "password": "user123", "is_active": True, "rol": "user"},
        ]

        for user_data in users_data:
            rut = user_data["rut"]
            password = user_data["password"]
            rol = user_data["rol"]
            is_active = user_data.get("is_active", True)

            user, created = Usuarios.objects.get_or_create(rut=rut)
            if created:
                user.set_password(password)
                user.is_active = is_active
                user.rol = rol
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Usuario {rut} creado correctamente."))
            else:
                self.stdout.write(f"Usuario {rut} ya existe. No se creó.")
