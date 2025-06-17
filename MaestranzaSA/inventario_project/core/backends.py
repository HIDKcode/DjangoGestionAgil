from django.contrib.auth.backends import BaseBackend
from core.models import Usuarios

class RutBackend(BaseBackend):
    def authenticate(self, request, usuario=None, clave=None):
        try:
            user = Usuarios.objects.get(rut=usuario)
            # Comparar clave texto plano (solo demo)
            if user.password == clave:
                return user
        except Usuarios.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None
