from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from RecaMan import settings
from RecaManApp.decorators import *
from RecaManApp.models import *
# Create your views here.
@check_user_roles('ADMIN')
def area_jefe(request):
    return render(request, 'AreaJefe.html')

def error(request):
    return render(request, 'errores.html')


def index(requerst):
    return render(requerst, 'index.html')

@check_user_roles('ADMIN')
def plantilla_mecanicos(request):
    list_mecanic = Mecanico.objects.all()
    return render(request, 'PlantillaMecanico.html',{'mecanico': list_mecanic})
def sobre_nosotros(request):
    return render(request, 'Sobre_nosotros.html')
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

        usuario = Usuario()
        usuario.nombreUsuario = nuevo.nombre.replace(" ", "")
        usuario.password = make_password(nuevo.dni)
        usuario.rol = Roles.MECANICO
        usuario.save()
        nuevo.user_id = usuario.id
        nuevo.save()

        return redirect('lista_mecanicos')

@check_user_roles('ADMIN')
def eliminar_mecanico(request, id):
    mecanic = Mecanico.objects.get(id=id)
    user = Usuario.objects.filter(id=mecanic.user_id).first()
    mecanic.delete()
    if user is not None:
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
        mecanic.user_id=user.id
        mecanic.save()

        return redirect('login')
    else:
        return redirect('plantillaMecanico')






def login_usuario(request):
    if request.method == "POST":
        NombreUsuario = request.POST.get('nombreusuario')
        contrasenya = request.POST.get('contraseña')

        usuario = authenticate(request, username=NombreUsuario, password=contrasenya)

        if usuario is not None and usuario.rol==Roles.ADMIN:
            login(request, usuario)

            return redirect('jefe')
        elif usuario is not None and usuario.rol==Roles.CLIENTE:
            login(request,usuario)
            return redirect('areausuario')
        else:

            return render(request, 'login.html', {"error": "No se ha podido iniciar sesión intentalo de nuevo"})


    return render(request, 'login.html')
def cerrar_sesion(request):
    logout(request)
    return redirect('login')

@check_user_roles('ADMIN')
def mostrar_citas(request):
    list_citas = Citas.objects.all()
    mecanicos = Mecanico.objects.all()
    if request.method == "GET":
        return render(request, 'listado_citas.html', {'citas': list_citas, 'mecanicos': mecanicos})
    else:
        cita = Citas()
        cita.hora = request.POST.get('hora')
        cita.mecanico = Mecanico.objects.get(id=request.POST.get('mecanicos'))
        cita.estado = EstadoCitas.ACEPTADA
        cita.save()
        return render(request, 'listado_citas.html')

@check_user_roles('ADMIN')
def plantilla_productos(request):
    list_product = Producto.objects.all()
    return render(request, 'PlantillaProducto.html', {'producto': list_product})


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
def nueva_marca(request):
    if request.method == 'GET':
        return render(request, 'newMarca.html')
    else:
        new = MarcaCoche()
        new.nombre = request.POST.get('nombre')
        new.url = request.POST.get('url')
        new.save()
        return redirect('añadir_marca')

@check_user_roles('ADMIN')
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


    try:
        cliente = Cliente.objects.get(user=usuario_logeado)
    except Cliente.DoesNotExist:

        return redirect('verificar')


    citas = Citas.objects.filter(cliente=cliente)

    return render(request, 'vistacitascliente.html', {'citas': citas})

@login_required
def eliminar_cita(request, id):
    cita = Citas.objects.get(id=id)
    cita.delete()
    return redirect('vistacitacliente')
@check_user_roles('ADMIN')
def nuevo_tipo_producto(request):
    if request.method == 'POST':
        new = Tipo_producto()
        new.nombre = request.POST.get('nombre')
        new.save()
        return redirect('añadir_tipo_producto')
    list_tipos_productos = Tipo_producto.objects.all()
    return render(request, 'newTipoProducto.html',{'tipos_productos': list_tipos_productos})

@check_user_roles('ADMIN')
def eliminar_tipo_producto(request, id):
    tipo_producto = Tipo_producto.objects.get(id=id)
    tipo_producto.delete()
    return redirect('añadir_tipo_producto')

@check_user_roles('ADMIN')
def editar_tipo_producto(request, id):
    tipo_producto = Tipo_producto.objects.get(id=id)
    list_tipos_productos = Tipo_producto.objects.all()
    if request.method == "GET":
        return render(request, 'newTipoProducto.html', {'tipo_producto':tipo_producto, 'tipos_productos':list_tipos_productos})
    else:
        tipo_producto.nombre = request.POST.get('nombre')
        tipo_producto.save()
        return redirect('añadir_tipo_producto')

@check_user_roles('ADMIN')
def mostrar_presupuestos(request):
    list_presupuestos = Presupuesto.objects.all()
    return render(request, 'listado_presupuestos.html', {'presupuesto': list_presupuestos})

@check_user_roles('ADMIN')
def mostrar_citas(request):
    list_citas = Citas.objects.all()
    mecanicos = Mecanico.objects.all()
    if request.method == "GET":
        return render(request, 'listado_citas.html', {'citas': list_citas, 'mecanicos': mecanicos})
    else:
        cita = Citas()
        cita.hora = request.POST.get('hora')
        cita.mecanico = Mecanico.objects.get(id=request.POST.get('mecanicos'))
        cita.estado = EstadoCitas.ACEPTADA
        cita.save()
        return render(request, 'listado_citas.html')

def pedir_cita(request):
    coches = CocheCliente.objects.filter(usuario=request.user)
    if request.method == 'GET':
        return render(request, 'newCitaCliente.html', {'coches': coches})
    else:
        usuario_logeado = request.user
        cliente = Cliente.objects.get(user=usuario_logeado)
        cita = Citas()
        cita.motivo = request.POST.get('motivo')
        cita.fecha = request.POST.get('fecha')
        cita.cocheCliente = CocheCliente.objects.get(id=request.POST.get('coche'))
        cita.estado = EstadoCitas.PENDIENTE
        cita.usuario = usuario_logeado
        cita.cliente = cliente
        cita.save()
        return redirect('añadir_cita_cliente')

def vista_citas_cliente(request):
    usuario_logeado = request.user
    try:
        cliente = Cliente.objects.get(user=usuario_logeado)
    except Cliente.DoesNotExist:
        return redirect('verificar')
    citas = Citas.objects.filter(cliente=cliente)
    return render(request, 'listado_citasCliente.html', {'citas': citas})
def eliminar_cita(request, id):
    cita = Citas.objects.get(id=id)
    cita.delete()
    return redirect('lista_citas_cliente')

@check_user_roles('CLIENTE')
def mostrar_coches(request):
    cocheCliente = CocheCliente.objects.all()
    for coche in cocheCliente:
        if coche.usuario.nombreUsuario != request.user.nombreUsuario:
            cocheCliente = cocheCliente.exclude(id=coche.id)
    return render(request, 'listado_cochesCliente.html', {'coches': cocheCliente})

@check_user_roles('CLIENTE')
def nuevo_coche(request):
    coche = CocheCliente.objects.all()
    if request.method == 'GET':
        return render(request, 'newCoche.html' ,{'coches': coche})
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
        return redirect('añadir_coche')

@check_user_roles('ADMIN')
def eliminar_tipo_producto(request, id):
    tipo_producto = Tipo_producto.objects.get(id=id)
    tipo_producto.delete()
    return redirect('añadir_tipo_producto')
@check_user_roles('ADMIN')
def editar_tipo_producto(request, id):
    tipo_producto = Tipo_producto.objects.get(id=id)
    list_tipos_productos = Tipo_producto.objects.all()
    if request.method == "GET":
        return render(request, 'newTipoProducto.html', {'tipo_producto':tipo_producto, 'tipos_productos':list_tipos_productos})
    else:
        tipo_producto.nombre = request.POST.get('nombre')
        tipo_producto.save()
        return redirect('añadir_tipo_producto')
@check_user_roles('ADMIN')
def mostrar_presupuestos(request):
    list_presupuestos = Presupuesto.objects.all()
    return render(request, 'listado_presupuestos.html', {'presupuesto': list_presupuestos})
@check_user_roles('CLIENTE')
def eliminar_coche(request,id):
    coche = CocheCliente.objects.get(id=id)
    coche.delete()
    return redirect('lista_coches')

@check_user_roles('CLIENTE')
def editar_coche(request, id):
    coche = CocheCliente.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'newCoche.html', {'coches':coche})
    else:
        usuario_logeado = request.user
        coche.modelo = request.POST.get('modelo')
        coche.marca = request.POST.get('marca')
        coche.matricula = request.POST.get('matricula')
        coche.KM = request.POST.get('kilometros')
        coche.ITV = request.POST.get('ITV')
        coche.usuario_id = usuario_logeado.id
        coche.save()
        return redirect('lista_coches')

@check_user_roles('CLIENTE')
def recambio_coche(request):
    return render(request,'recambio_coche.html')

def nuevo_presupuesto(request):
    list_citas = Citas.objects.filter(mecanico_id=request.user.id)
    if request.method == 'GET':
        return render(request, 'newPresupuesto.html', {'citas': list_citas})
    else:
        new = Presupuesto()
        new.cita = Citas.objects.get(id=request.POST.get('cita'))
        new.fallos = request.POST.get('fallos')
        new.precio = request.POST.get('precio')
        new.fecha_compra = new.cita.fecha
        new.cliente_id = new.cita.cliente_id
        new.save()
        return redirect('listado_presupuestos')

def buscador(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.all()
    return render(request, 'tienda.html', {'producto': productos})

def lista_productos_tienda(request):
    productos = Producto.objects.all()
    return render(request, 'tienda.html', {'producto': productos})

@check_user_roles('CLIENTE')
def add_to_cart(request, id):
    cart = {}

    # Comprobar si hay ya un carrito en sesión
    if "cart" in request.session:
        cart = request.session.get("cart", {})

    # Comprobar que el producto está o no está en el carrito
    if str(id) in cart.keys():
        cart[str(id)] = cart[str(id)] + 1
    else:
        cart[str(id)] = 1

    request.session["cart"] = cart

    return redirect('tienda')

@check_user_roles('CLIENTE')
def show_cart(request):
    cart = {}
    session_cart = {}
    total = 0.0

    if 'cart' in request.session:
        session_cart = request.session.get('cart', {})

    for key in session_cart.keys():
        product = Producto.objects.get(id=key)
        amount = session_cart[key]
        cart[product] = amount
        total += amount * product.precio

    return render(request, 'cart.html', {'cart': cart, 'total': total})
@check_user_roles('CLIENTE')
def eliminar_producto_carrito(request, id):
    # Comprobar si hay ya un carrito en sesión
    if "cart" in request.session:
        cart = request.session.get("cart", {})

        # Comprobar que el producto está en el carrito
        if str(id) in cart.keys():
            del cart[str(id)]  # eliminar el producto del carrito

        request.session["cart"] = cart  # guardar el carrito actualizado en la sesión

    return redirect('show_cart')

@check_user_roles('CLIENTE')
def incrementar_carrito(request, producto_id):
    cart = {}

    # Comprobar si hay ya un carrito en sesión
    if "cart" in request.session:
        cart = request.session.get("cart", {})

    # Comprobar que el producto está o no está en el carrito
    if str(producto_id) in cart.keys():
        cart[str(producto_id)] = cart[str(producto_id)] + 1

    request.session["cart"] = cart

    return redirect('show_cart')

@check_user_roles('CLIENTE')
def disminuir_carrito(request, producto_id):
    cart = {}

    # Comprobar si hay ya un carrito en sesión
    if "cart" in request.session:
        cart = request.session.get("cart", {})

    # Comprobar que el producto está o no está en el carrito
    if str(producto_id) in cart.keys():
        if cart[str(producto_id)] > 1:
            cart[str(producto_id)] = cart[str(producto_id)] - 1

    request.session["cart"] = cart

    return redirect('show_cart')


def contacto(request):
   if request.method == 'POST':
       nombre = request.POST.get('nombre')
       mail = request.POST.get('mail')
       direccion = request.POST.get('direccion')
       fecha = request.POST.get('fecha')

       templete = render_to_string('email_template.html', {'nombre': nombre, 'mail': mail, 'direccion': direccion, 'fecha': fecha})

       mail = EmailMessage(
              'Gracias por contactar con nosotros',
           templete,
           settings.EMAIL_HOST_USER,

           [mail]
       )

       mail.fail_silently = False

       mail.send()

       messages.success(request, 'Mensaje enviado correctamente')

       return redirect('verificar')