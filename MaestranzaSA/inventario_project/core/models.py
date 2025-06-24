from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings
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
    def create_user(self, rut, password=None, **extra_fields):
        if not rut:
            raise ValueError("El RUT es obligatorio")
        user = self.model(rut=rut, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rut, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'admin')

        if not extra_fields.get('is_staff'):
            raise ValueError("Superusuario debe tener is_staff=True")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superusuario debe tener is_superuser=True")

        return self.create_user(rut, password, **extra_fields)

class Usuarios(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('admin', 'Administrador'),
        ('inventario', 'Gestor de Inventario'),
        ('comprador', 'Comprador'),
        ('logistica', 'Encargado de Logística'),
        ('produccion', 'Jefe de Producción'),
        ('auditor', 'Auditor de Inventario'),
        ('gerente', 'Gerente de Proyectos'),
        ('planta', 'Usuario Planta'),
    ]

    rut = models.CharField(max_length=12, primary_key=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='planta')
    intentos_fallidos = models.IntegerField(default=0)
    bloqueado = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.rut
    

class MovimientoInventario(models.Model):
    ACCIONES = [
        ('CREADO', 'Creado'),
        ('EDITADO', 'Editado'),
        ('ASIGNADO', 'Asignado'),
        ('AJUSTE', 'Ajuste manual'),
    ]

    pieza = models.ForeignKey(Piezas, on_delete=models.CASCADE)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    cantidad = models.IntegerField(null=True, blank=True) 
    usuario = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
)
    fecha = models.DateTimeField(default=timezone.now)
    observacion = models.TextField(blank=True)

    class Meta:
        db_table = 'movimiento_inventario'

    def __str__(self):
        return f"{self.pieza.nombre} - {self.accion} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
    
class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    piezas = models.ManyToManyField('Piezas', through='AsignacionPieza')
    class Meta:
        db_table = 'proyectos'

class AsignacionPieza(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    pieza = models.ForeignKey(Piezas, on_delete=models.CASCADE)  # ojo que aquí es 'pieza' (singular)
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        
        unique_together = ('proyecto', 'pieza')