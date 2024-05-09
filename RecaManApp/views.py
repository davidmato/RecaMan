from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from RecaManApp.decorators import check_user_roles
from RecaManApp.models import Mecanico, Usuario, Producto, Citas, MarcaCoche, Tipo_producto, Roles, CocheCliente, \
    Cliente, EstadoCita
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect


# Create your views here
# .
@check_user_roles('ADMIN')
def area_jefe(request):
    return render(request, 'newMecanic.html')

def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')

def error(request):
    return render(request, 'errores.html')

@check_user_roles('ADMIN')
def plantillamecanic(request):
    list_mecanic = Mecanico.objects.all()
    return render(request, 'PlantillaMecanico.html',{'mecanico': list_mecanic})

@check_user_roles('ADMIN')
def mostrar_citas(request):
    list_citas = Citas.objects.all()
    mecanicos = Mecanico.objects.all()

    if request.method == "GET":
        return render(request, 'lista_citas.html', {'citas': list_citas, 'mecanicos' : mecanicos})

    else:

         cita = Citas()
         cita.hora = request.POST.get('hora')
         cita.mecanico = Mecanico.objects.get(id=request.POST.get('mecanicos'))
         cita.estado = EstadoCita.ACEPTADA
         cita.save()
         return render(render, 'lista_citas.html')


@check_user_roles('ADMIN')
def asignar_Usuario(request):
    usuario_logeado = Usuario.objects.get(nombreUsuario=request.user.nombreUsuario)
    cliente = None

    if usuario_logeado is not None and usuario_logeado.rol == Roles.CLIENTE:
        clientes = Cliente.objects.filter(user=usuario_logeado)

        if len(clientes) != 0:
            cliente = clientes[0]
        if request.method == "GET":
            if cliente is not None:
                return render(request, 'verificarCliente.html')
            else:
                return render(request, 'verificarCliente.html')

        else:

            if "verificar" in request.POST:
                cliente = Cliente()

            cliente.nombre = request.POST.get('nombre')
            cliente.email = request.POST.get('mail')
            cliente.direccion = request.POST.get('direccion')
            cliente.fecha_nacimiento = request.POST.get('fecha')
            cliente.user = usuario_logeado
            cliente.save()

            return render(request, 'verificarCliente.html')


@login_required
def areaUsuario(request):
    usuario_logeado = request.user

    try:
        cliente = Cliente.objects.get(user=usuario_logeado)
    except Cliente.DoesNotExist:
        cliente = None

    return render(request, 'areaUsuario.html', {'cliente': cliente})
def pedir_cita(request):
    if request.method == 'GET':
        return render(request, 'pedircita.html')
    else:
        usuario_logeado = request.user
        cliente = Cliente.objects.get(user=usuario_logeado)
        cita = Citas()
        cita.motivo = request.POST.get('motivo')
        cita.fecha = request.POST.get('fecha')
        cita.estado = EstadoCita.PENDIENTE
        cita.cliente = cliente
        cita.save()

        return redirect('pedircita')


@check_user_roles('ADMIN')
def nueva_marca(request):
    if request.method == 'GET':
        return render(request, 'newMarca.html')
    else:
        new = MarcaCoche()
        new.nombre = request.POST.get('nombre')
        new.url = request.POST.get('url')
        new.save()
        return redirect('añadir_marca')
def mostrar_marcas(request):
    list_marcas = MarcaCoche.objects.all()
    return render(request, 'listado_marcas.html', {'marcas': list_marcas})
@check_user_roles('ADMIN')
def eliminar_marca(request, id):
    marca = MarcaCoche.objects.get(id=id)
    marca.delete()
    return redirect('lista_marcas')
@check_user_roles('ADMIN')
def editar_marca(request, id):
    marca = MarcaCoche.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'newMarca.html', {'marca':marca})
    else:
        marca.nombre = request.POST.get('nombre')
        marca.url = request.POST.get('url')
        marca.save()
        return redirect('lista_marcas')

def vistacitacliente(request):
    usuario_logeado = request.user


    cliente = Cliente.objects.get(user=usuario_logeado)


    citas = Citas.objects.filter(cliente=cliente)

    return render(request, 'vistacitascliente.html', {'citas': citas})

def eliminar_cita(request, id):
    cita = Citas.objects.get(id=id)
    cita.delete()
    return redirect('vistacitacliente')
def footer(request):
    return render(request, 'footer.html')

def header(request):
    return render(request, 'header_admin.html')
@check_user_roles('ADMIN')
def plantilla_mecanicos(request):
    list_mecanic = Mecanico.objects.all()
    return render(request, 'PlantillaMecanico.html',{'mecanico': list_mecanic})
@check_user_roles('ADMIN')
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
@check_user_roles('ADMIN')
def eliminar_mecanico(request, id):
    mecanic = Mecanico.objects.get(id=id)
    user = Usuario.objects.get(id=mecanic.user_id)
    mecanic.delete()
    user.delete()
    return redirect('lista_mecanicos')
@check_user_roles('ADMIN')
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
        NameUsuario = request.POST.get('nom-usuario')
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
            user = Usuario.objects.create(nombreUsuario=NameUsuario, password=make_password(password))
            user.save()
            return redirect('login')
@check_user_roles('ADMIN')
def mostrar_citas(request):
    list_citas = Citas.objects.all()
    return render(request, 'listado_citas.html', {'citas': list_citas})
@check_user_roles('ADMIN')
def plantilla_productos(request):
    list_product = Producto.objects.all()
    return render(request, 'PlantillaProducto.html', {'producto': list_product})
@check_user_roles('ADMIN')
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
@check_user_roles('ADMIN')
def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('lista_productos')
@check_user_roles('ADMIN')
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
@check_user_roles('ADMIN')
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

        if usuario is not None and usuario.rol==Roles.ADMIN:
            login(request, usuario)

            return redirect('añadir_mecanico')
        elif usuario is not None and usuario.rol==Roles.CLIENTE:
            login(request,usuario)
            return redirect('areausuario')
        else:

            return render(request, 'login.html', {"error": "No se ha podido iniciar sesión intentalo de nuevo"})


    return render(request, 'login.html')



def listado_coches(request):
    cocheCliente = CocheCliente.objects.get(id=request.user.id)
    return render(request, 'listado_coches.html', {'coches': cocheCliente})
@check_user_roles('CLIENTE')
def nuevo_coche(request):
    coche = CocheCliente.objects.all()
    if request.method == 'GET':
        return render(request, 'newCoches.html' ,{'coches': coche})
    else:
        usuario_logeado = request.user
        coche = CocheCliente()
        coche.modelo = request.POST.get('modelo')
        coche.marca = request.POST.get('marca')
        coche.matricula = request.POST.get('matricula')
        coche.KM = request.POST.get('kilometros')
        coche.ITV = request.POST.get('ITV')
        coche.usuario_id = usuario_logeado.id
        coche.save()
        return redirect('mis_coches')
@check_user_roles('CLIENTE')

def eliminar_coche(request,id):
    coche = CocheCliente.objects.get(id=id)
    coche.delete()
    return redirect('mis_coches')

@check_user_roles('CLIENTE')
def editar_coche(request, id):
    coche = CocheCliente.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'newCoches.html', {'coches':coche})
    else:
        usuario_logeado = request.user
        coche.modelo = request.POST.get('modelo')
        coche.marca = request.POST.get('marca')
        coche.matricula = request.POST.get('matricula')
        coche.KM = request.POST.get('kilometros')
        coche.ITV = request.POST.get('ITV')
        coche.usuario_id = usuario_logeado.id
        coche.save()
        return redirect('mis_coches')
@check_user_roles('CLIENTE')
def recambio_coche(request):
    return render(request,'recambio_coche.html')