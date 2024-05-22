from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class MarcaCoche(models.Model):
    nombre = models.CharField(max_length=150)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre + ' ' + self.url


class Tipo_producto(models.Model):
    nombre = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre + '' + self.url

class EstadoCitas(models.TextChoices):
    PENDIENTE = 'PENDIENTE', 'Pendiente'
    FINALIZADA = 'FINALIZADA', 'Finalizada'
    ACEPTADA = 'ACEPTADA', 'Aceptada'
    RECHAZADA = 'RECHAZADA', 'Rechazada'

class Roles(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrador'
    MECANICO = 'MECANICO','Mecanico'
    CLIENTE = 'CLIENTE', 'Cliente'


class UserManager(BaseUserManager):
    def create_user(self, mail,password=None, **extra_fields):
        if not mail:
            raise ValueError('El email es un campo obligatorio')
        user = self.normalize_email(mail)
        user = self.model(mail=mail, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, mail, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True')

        return self.create_user(mail, password, **extra_fields)


class Producto (models.Model):
    nombre = models.CharField(max_length=150)
    url = models.CharField(max_length=500)
    precio = models.FloatField()
    descripcion = models.CharField(max_length=250)
    marca = models.ForeignKey(MarcaCoche, on_delete=models.CASCADE)
    tipo_producto = models.ForeignKey(Tipo_producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + ' ' + self.url + ' ' + str(self.precio) + ' ' + self.descripcion + ' ' + str(self.marca) + ' ' + str(self.tipo_producto)


class Usuario(AbstractBaseUser):
    nombreUsuario = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    rol = models.CharField(max_length=15, choices=Roles.choices, default=Roles.CLIENTE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'nombreUsuario'
    REQUIRED_FIELDS = ['password', 'email']

    def __str__(self):
        return self.nombreUsuario + ' ' + self.password + ' '

class Cliente (models.Model):
    nombre = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    user = models.ForeignKey(Usuario, null=True, on_delete=models.DO_NOTHING)
    producto = models.ManyToManyField(Producto)

    def __str__(self):
        return self.nombre + ' ' + self.nombreUsuario + ' ' + self.email + ' ' + self.password + ' ' + self.direccion + ' ' + str(self.producto)

class Mecanico (models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(max_length=9)
    url = models.CharField(max_length=500)
    user = models.OneToOneField(Usuario, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre + ' ' + self.email + ' ' + str(self.fecha_nacimiento) + ' ' + self.dni + ' ' + self.url


class CocheCliente(models.Model):
    modelo = models.CharField(max_length=150)
    matricula = models.CharField(max_length=7)
    KM = models.IntegerField()
    ITV = models.BooleanField()
    marca = models.CharField(max_length=150)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.modelo + ' ' + self.matricula + ' ' + str(self.KM) + ' ' + str(self.ITV) + ' ' + str(self.marca) + ' ' + str(self.usuario)


class Citas (models.Model):
    fecha = models.DateField()
    hora = models.TimeField(null=True)
    motivo = models.CharField(max_length=250)
    estado = models.CharField(max_length=15, choices=EstadoCitas.choices, default=EstadoCitas.PENDIENTE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mecanico = models.ForeignKey(Mecanico, on_delete=models.CASCADE, null=True)
    cocheCliente = models.ForeignKey(CocheCliente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha) + ' ' + str(self.hora) + ' ' + self.motivo + ' ' + str(self.usuario) + ' ' + str(self.mecanico) + ' ' + str(self.cocheCliente)


class Presupuesto (models.Model):
    fecha_compra = models.DateField()
    fallos = models.CharField(max_length=500, null=True)
    precio = models.FloatField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto)
    cita = models.ForeignKey(Citas, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.fecha_compra) + ' ' + str(self.precio) + ' ' + str(self.usuario) + ' ' + str(self.cita) + ' ' + str(self.producto)


class Comentario (models.Model):
    puntuacion = models.IntegerField()
    comentario = models.CharField(max_length=250)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.puntuacion) + ' ' + self.comentario + ' ' + str(self.usuario) + ' ' + str(self.producto)

class LineaPedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.FloatField()

    def __str__(self):
        return str(self.producto) + ' ' + str(self.cantidad) + ' ' + str(self.precio)


class Pedido(models.Model):
    codigo = models.CharField(max_length=100, blank=False)
    fecha = models.DateField(null=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    linea_pedidos = models.ManyToManyField(LineaPedido)

    def __str__(self):
        return self.codigo + ' ' + str(self.fecha) + ' ' + str(self.cliente) + ' ' + str(self.linea_pedidos)
