from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class Errores(models.Model):
    id = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', on_delete=models.SET_NULL, blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)
    origen_html = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'errores'


class Kits(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'kits'


class KitsPiezas(models.Model):
    id = models.BigAutoField(primary_key=True)
    kit = models.ForeignKey(Kits, on_delete=models.SET_NULL, null=True)
    pieza = models.ForeignKey('Piezas', on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()

    class Meta:
        db_table = 'kits_piezas'


class Ordenes(models.Model):
    id = models.BigAutoField(primary_key=True)
    pieza = models.ForeignKey('Piezas', on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    fecha_creacion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    aprobado_por = models.ForeignKey('Usuarios', on_delete=models.SET_NULL, db_column='aprobado_por', blank=True, null=True)

    class Meta:
        db_table = 'ordenes'


class Piezas(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    umbral_minimo = models.IntegerField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    proveedor = models.ForeignKey('Proveedores', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'piezas'


class PreciosAnteriores(models.Model):
    id = models.BigAutoField(primary_key=True)
    pieza = models.ForeignKey(Piezas, on_delete=models.SET_NULL, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_actualizacion = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'precios_anteriores'


class Proveedores(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255, blank=True, null=True)
    condiciones_pago = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'proveedores'


class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, clave=None, **extra_fields):
        if not usuario:
            raise ValueError("El usuario debe tener un nombre de usuario")
        user = self.model(usuario=usuario, **extra_fields)
        user.set_password(clave)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, clave, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser debe tener is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser debe tener is_superuser=True")

        return self.create_user(usuario, clave, **extra_fields)

class Usuarios(AbstractBaseUser, PermissionsMixin):
    usuario = models.CharField(max_length=255, unique=True)
    rut = models.CharField(max_length=12, unique=True)
    contrasena = models.CharField(max_length=128) ## Debemos encritparlo más tarde
    rol = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    intentos_fallidos = models.IntegerField(blank=True, null=True)
    bloqueado = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.usuario