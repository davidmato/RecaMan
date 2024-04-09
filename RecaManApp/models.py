from django.db import models

# Create your models here.
class marcaCoche(models.Model):
    nombre = models.CharField(max_length=150)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre + ' ' + self.url

class tipo_producto(models.Model):
    liquido_mantenimiento = models.CharField(max_length=250)
    sistema_motor = models.CharField(max_length=250)
    sistema_frenos = models.CharField(max_length=250)
    articulos_no_mecanicos = models.CharField(max_length=250)
    sistema_refrigeracion = models.CharField(max_length=250)

    def __str__(self):
        return self.liquido_mantenimiento + ' ' + self.sistema_motor + ' ' + self.sistema_frenos + ' ' + self.articulos_no_mecanicos + ' ' + self.sistema_refrigeracion

class producto (models.Model):
    nombre = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=200)
    marca = models.ForeignKey(marcaCoche, on_delete=models.CASCADE)
    tipo_producto = models.ForeignKey(tipo_producto, on_delete=models.CASCADE)

class Usuario(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    nombreUsuario = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    producto = models.ManyToManyField(producto)

    def __str__(self):
        return self.nombre + ' ' + self.apellido + ' ' + self.nombreUsuario + ' ' + self.email + ' ' + self.password + ' ' + self.direccion


class mecanico (models.Model):
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
    marca = models.ForeignKey(marcaCoche, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


    def __str__(self):
        return self.modelo + ' ' + self.matricula + ' ' + str(self.KM) + ' ' + str(self.ITV) + ' ' + str(self.marca) + ' ' + str(self.usuario)

class citas (models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=200)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mecanico = models.ForeignKey(mecanico, on_delete=models.CASCADE)
    cocheCliente = models.ForeignKey(CocheCliente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha) + ' ' + str(self.hora) + ' ' + self.motivo + ' ' + str(self.usuario) + ' ' + str(self.mecanico) + ' ' + str(self.CocheCliente)
class presupuesto (models.Model):
    fecha_compra = models.TimeField()
    precio = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ManyToManyField(producto)
    cita = models.ForeignKey(citas, on_delete=models.CASCADE)



    def __str__(self):
        return self.fecha_compra + ' ' + str(self.precio) + ' ' + str(self.usuario) + ' ' + str(self.cita) + ' ' + str(self.producto)


class fallos (models.Model):
    descripcion = models.CharField(max_length=200)
    presupuesto = models.ForeignKey(presupuesto, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion + ' ' + str(self.presupuesto)

class comentario (models.Model):
    puntuacion = models.IntegerField()
    comentario = models.CharField(max_length=200)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.puntuacion) + ' ' + self.comentario + ' ' + str(self.usuario) + ' ' + str(self.producto)
