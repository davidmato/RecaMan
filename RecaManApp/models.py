

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class MarcaCoche(models.Model):
    nombre = models.CharField(max_length=150)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre + ' ' + self.url


class Tipo_producto(models.Model):
    nombre = models.CharField(max_length=150)


    def __str__(self):
        return self.nombre

class EstadoCita(models.TextChoices):
    PENDIENTE = 'PENDIENTE','Pendiente'
    FINALIZADA = 'FINALIZADA','Finalizada'
    ACEPTADA = 'ACEPTADA', 'Aceptada'
    RECHAZADA = 'RECHAZADA','Rechazada'


class Roles(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrador'
    MECANICO = 'MECANICO','Mecanico'
    CLIENTE = 'CLIENTE', 'Cliente'


class UserManager(BaseUserManager):
    def create_user(self, mail,password=None, **extra_fields):
        if not mail:
            raise ValueError('El email es un campo obligatorio')
        mail = self.normalize_email(mail)
        user = self.model(email=mail, **extra_fields)
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
    nombre = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=200)
    marca = models.ForeignKey(MarcaCoche, on_delete=models.CASCADE)
    tipo_producto = models.ForeignKey(Tipo_producto, on_delete=models.CASCADE)
    precio = models.FloatField()

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
        return  self.nombreUsuario + ' '  + self.password + ' '



class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    user = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, default=None)
    producto = models.ManyToManyField(Producto)

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
    matricula = models.CharField(max_length=150)
    KM = models.IntegerField()
    ITV = models.BooleanField()
    marca = models.ForeignKey(MarcaCoche, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)


    def __str__(self):
        return self.modelo + ' ' + self.matricula + ' ' + str(self.KM) + ' ' + str(self.ITV) + ' ' + str(self.marca) + ' ' + str(self.cliente)

class Citas (models.Model):
    fecha = models.DateField()
    hora = models.TimeField(null=True)
    motivo = models.CharField(max_length=200)
    estado = models.CharField(max_length=15, choices=EstadoCita.choices, default=EstadoCita.PENDIENTE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mecanico = models.ForeignKey(Mecanico, on_delete=models.CASCADE, null=True)
    cocheCliente = models.ForeignKey(CocheCliente, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.fecha) + ' ' + str(self.hora) + ' ' + self.motivo + ' ' + str(self.cliente) + ' ' + str(self.mecanico) + ' ' + str(self.cocheCliente)
class Presupuesto (models.Model):
    fecha_compra = models.DateField()
    precio = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto)
    cita = models.ForeignKey(Citas, on_delete=models.CASCADE)



    def __str__(self):
        return str(self.fecha_compra) + ' ' + str(self.precio) + ' ' + str(self.cliente) + ' ' + str(self.cita) + ' ' + str(self.producto)


class Fallos (models.Model):
    descripcion = models.CharField(max_length=200)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion + ' ' + str(self.presupuesto)

class Comentario (models.Model):
    puntuacion = models.IntegerField()
    comentario = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.puntuacion) + ' ' + self.comentario + ' ' + str(self.cliente) + ' ' + str(self.producto)
