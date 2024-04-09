from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    nombreUsuario = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    rol = models.CharField(max_length=150)
    metodoPago = models.CharField(max_length=150)


    def __str__(self):
        return self.nombre + ' ' + self.apellido + ' ' + self.nombreUsuario + ' ' + self.email + ' ' + self.password + ' ' + self.direccion + ' ' + self.rol



class marcaCoche(models.Model):
    nombre = models.CharField(max_length=150)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre + ' ' + self.url


class CocheCliente(models.Model):
    modelo = models.CharField(max_length=150)
    matricula = models.CharField(max_length=150)
    KM = models.IntegerField()
    descripcion_fallo = models.CharField(max_length=200)
    ITV = models.BooleanField()
    marca = models.ForeignKey(marcaCoche, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


    def __str__(self):
        return self.modelo + ' ' + self.matricula + ' ' + str(self.KM) + ' ' + self.descripcion_fallo + ' ' + str(self.ITV) + ' ' + str(self.marca) + ' ' + str(self.usuario)
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
    tipo_producto = models.ForeignKey(tipo_producto, on_delete=models.CASCADE)
    marca = models.ForeignKey(marcaCoche, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + ' ' + str(self.url) + ' ' + self.descripcion + ' ' + str(self.tipo_producto) + ' ' + str(self.marca)


class citas (models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=200)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha) + ' ' + str(self.hora) + ' ' + self.motivo + ' ' + str(self.usuario)

class presupuesto (models.Model):
    fallos = models.CharField(max_length=200)
    precio = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.fallos + ' ' + str(self.precio) + ' ' + str(self.usuario)

class presupuesto_producto (models.Model):
    presupuesto = models.ManyToManyField(presupuesto)
    producto = models.ManyToManyField(producto)

    def __str__(self):
        return str(self.presupuesto) + ' ' + str(self.producto)

class presupuesto_cocheCliente (models.Model):
    presupuesto = models.ManyToManyField(presupuesto)
    cocheCliente = models.ManyToManyField(CocheCliente)

    def __str__(self):
        return str(self.presupuesto) + ' ' + str(self.cocheCliente)

class valoracion (models.Model):
    producto = models.ManyToManyField(producto)
    usuario = models.ManyToManyField(Usuario)

    def __str__(self):
        return str(self.producto) + ' ' + str(self.usuario)

class mecanico (models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(max_length=9)
    cita = models.ForeignKey(citas, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + ' ' + self.email + ' ' + str(self.fecha_nacimiento) + ' ' + self.dni + ' ' + str(self.cita)