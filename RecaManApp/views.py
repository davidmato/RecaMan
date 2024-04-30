from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from RecaManApp.models import *
# Create your views here.
def area_jefe(request):
    return render(request, 'newMecanic.html')

def plantilla_mecanicos(request):
    list_mecanic = Mecanico.objects.all()
    return render(request, 'PlantillaMecanico.html',{'mecanico': list_mecanic})

def nuevo_meacanico(request):
    if request.method == 'GET':
        return render(request, 'newMecanic.html')
    else:
        nuevo = Mecanico()
        nuevo.nombre = request.POST.get('mecanicnamen')
        nuevo.email = request.POST.get('mail')
        nuevo.fecha_nacimiento = request.POST.get('birth')
        nuevo.dni = request.POST.get('dni')
        nuevo.url = request.POST.get('url')
        nuevo.save()
        return redirect('añadir_mecanico')

def eliminar_mecanico(request, id):
    mecanic = Mecanico.objects.get(id=id)
    mecanic.delete()
    return redirect('lista_mecanicos')

def editar_mecanico(request, id):
    mecanic = Mecanico.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'newMecanic.html', {'mecanic':mecanic})
    else:
        mecanic.nombre = request.POST.get('mecanicnamen')
        mecanic.email = request.POST.get('mail')
        mecanic.fecha_nacimiento = request.POST.get('birth')
        mecanic.dni = request.POST.get('dni')
        mecanic.url = request.POST.get('url')
        mecanic.save()
        return redirect('lista_mecanicos')

#FALTA TERMINAR DE REDIRIGIR BIEN LA PAGINA A LAS AREAS CORRESPONDIENTES
def registrar_usuario(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        name = request.POST.get('nombre-registro')
        mail = request.POST.get('email-registro')
        NameUsuario = request.POST.get('nom-usuario')
        dicrection = request.POST.get('register-direccion')
        fecha = request.POST.get('fecha-nacimiento')
        password = request.POST.get('contraseña-registro')
        repeatpassword = request.POST.get('confirmar')
        errores = []
        if password != repeatpassword:
            errores.append('Las contraseñas no coinciden')
        existe_usuario = Usuario.objects.filter(nombreUsuario=NameUsuario).exists()
        if existe_usuario:
            errores.append('Ya existe el nombre de ese usuario')
        if len(errores) != 0:
            return render(request, 'register.html', {'errores':errores})
        else:
            user = Usuario.objects.create(nombreUsuario=NameUsuario, password=make_password(password), email=mail)
            cliente = Cliente.objects.create(nombre=name, direccion=dicrection, fecha_nacimiento=fecha)
            cliente.nombre = name
            cliente.fecha_nacimiento = fecha
            cliente.direccion = dicrection
            user.nombre=name
            user.save()
            cliente.save()
            return redirect('lista_mecanicos')

def mostrar_citas(request):
    list_citas = Citas.objects.all()
    return render(request, 'listado_citas.html', {'citas': list_citas})

def plantilla_productos(request):
    list_product = Producto.objects.all()
    return render(request, 'PlantillaProducto.html', {'producto': list_product})

def nuevo_producto(request):
    if request.method == 'GET':
        tipos_producto = Tipo_producto.objects.all()
        marca = MarcaCoche.objects.all()
        return render(request, 'newProduct.html', {'tipos_producto': tipos_producto, 'marca': marca})
    else:

        new = Producto()
        new.nombre = request.POST.get('nombre')
        new.url = request.POST.get('url')
        new.descripcion = request.POST.get('descripcion')
        new.marca = MarcaCoche.objects.get(id=request.POST.get('marca'))
        new.tipo_producto = Tipo_producto.objects.get(id=request.POST.get('tipos_producto'))
        new.precio = request.POST.get('precio', 0.0)
        new.save()

        return redirect('añadir_producto')

def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('lista_productos')

def editar_producto(request, id):
    producto = Producto.objects.get(id=id)
    tipos_producto = Tipo_producto.objects.all()
    marca = MarcaCoche.objects.all()
    if request.method == 'GET':
        return render(request, 'newProduct.html', {'producto': producto, 'tipos_producto': tipos_producto, 'marca':marca})
    else:
        producto.nombre = request.POST.get('nombre')
        producto.url = request.POST.get('url')
        producto.descripcion = request.POST.get('descripcion')
        producto.marca = MarcaCoche.objects.get(id=request.POST.get('marca'))
        producto.tipo_producto = Tipo_producto.objects.get(id=request.POST.get('tipos_producto'))
        producto.precio = request.POST.get('precio', 0.0)
        producto.save()


        return redirect('lista_productos')

def registrar_mecanico_usuario(request, id):
    mecanic = Mecanico.objects.get(id=id)

    if mecanic.user is None:
        user = Usuario()
        user.nombre = mecanic.nombre.replace(" ","")
        user.nombreUsuario = mecanic.nombre.replace(" ","")
        user.email = mecanic.email
        user.password = make_password(mecanic.dni)
        user.rol = Roles.MECANICO
        user.save()
        mecanic.user_id = user.id
        mecanic.save()
        return redirect('login')
    else:
        return redirect('plantilla_mecanicos')

def login_usuario(request):
    if request.method == "POST":
        NombreUsuario = request.POST.get('nombreusuario')
        contrasenya = request.POST.get('contraseña')

        usuario = authenticate(request, username=NombreUsuario, password=contrasenya)

        if usuario is not None:
            login(request, usuario)

            return redirect('newMecanic')
        else:

            return render(request, 'login.html', {"error": "No se ha podido iniciar sesión intentalo de nuevo"})


    return render(request, 'login.html')

