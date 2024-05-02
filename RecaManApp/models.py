
from django.db import models

# Create your models here.
class MarcaCoche(models.Model):
    nombre = models.CharField(max_length=150)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre + ' ' + self.url

class Tipo_producto(models.Model):
    tipo = models.CharField(max_length=250)

    def __str__(self):
        return self.tipo
class Producto (models.Model):
    nombre = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=200)
    marca = models.ForeignKey(MarcaCoche, on_delete=models.CASCADE)
    tipo_producto = models.ForeignKey(Tipo_producto, on_delete=models.CASCADE)

class Usuario(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    nombreUsuario = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    producto = models.ManyToManyField(Producto)

    def __str__(self):
        return self.nombre + ' ' + self.apellido + ' ' + self.nombreUsuario + ' ' + self.email + ' ' + self.password + ' ' + self.direccion


class Mecanico (models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(max_length=9)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre + ' ' + self.email + ' ' + str(self.fecha_nacimiento) + ' ' + self.dni + ' ' + self.url
class CocheCliente(models.Model):
    modelo = models.CharField(max_length=150)
    matricula = models.CharField(max_length=150)
    KM = models.IntegerField()
    ITV = models.BooleanField()
    marca = models.ForeignKey(MarcaCoche, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)



class Citas (models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=200)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mecanico = models.ForeignKey(Mecanico, on_delete=models.CASCADE)
    cocheCliente = models.ForeignKey(CocheCliente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha) + ' ' + str(self.hora) + ' ' + self.motivo + ' ' + str(self.usuario) + ' ' + str(self.mecanico) + ' ' + str(self.cocheCliente)
class Presupuesto (models.Model):
    fecha_compra = models.TimeField()
    precio = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto)
    cita = models.ForeignKey(Citas, on_delete=models.CASCADE)



    def __str__(self):
        return str(self.fecha_compra) + ' ' + str(self.precio) + ' ' + str(self.usuario) + ' ' + str(self.cita) + ' ' + str(self.producto)


class Fallos (models.Model):
    descripcion = models.CharField(max_length=200)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion + ' ' + str(self.presupuesto)

class Comentario (models.Model):
    puntuacion = models.IntegerField()
    comentario = models.CharField(max_length=200)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.puntuacion) + ' ' + self.comentario + ' ' + str(self.usuario) + ' ' + str(self.producto)
