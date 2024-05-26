import time
from datetime import datetime
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import Sum, ExpressionWrapper, F, FloatField
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from RecaMan import settings
from RecaManApp.decorators import *
from RecaManApp.models import *
# Create your views here.
def inicio(request):
    list_product = Producto.objects.all().order_by('?')[:10]
    single_mecanico = Mecanico.objects.all().order_by('?')[:3]
    return render(request, 'index.html', {'producto': list_product, 'single_mecanico': single_mecanico})

@check_user_roles('ADMIN')
def area_jefe(request):
    return render(request, 'AreaJefe.html')

def error(request):
    return render(request, 'errores.html')

@check_user_roles('ADMIN')
def plantilla_mecanicos(request):
    list_mecanic = Mecanico.objects.all()
    return render(request, 'PlantillaMecanico.html',{'mecanico': list_mecanic})

@check_user_roles('ADMIN')
def nuevo_meacanico(request):
    mecanico = Mecanico.objects.all()
    if request.method == 'GET':
        return render(request, 'newMecanic.html')
    else:
        nuevo = Mecanico()
        nuevo.nombre = request.POST.get('mecanicnamen')
        nuevo.email = request.POST.get('mail')
        nuevo.fecha_nacimiento = request.POST.get('birth')
        nuevo.dni = request.POST.get('dni')
        nuevo.url = request.POST.get('url')
        usuario = Usuario()
        usuario.nombreUsuario = nuevo.nombre.replace(" ","")
        usuario.password = make_password(nuevo.dni)
        usuario.rol = Roles.MECANICO
        usuario.save()
        nuevo.user_id = usuario.id
        nuevo.save()
        return render(request, 'PlantillaMecanico.html', {'mecanico': mecanico,
                                                   'alert': {'icon': 'success',
                                                             'message': 'Mecanico añadido correctamente '}})


@check_user_roles('ADMIN')
def eliminar_mecanico(request, id):
    mecanic = Mecanico.objects.get(id=id)
    user = Usuario.objects.get(id=mecanic.user_id)
    mecanico = Mecanico.objects.all()
    mecanic.delete()
    if user is not None:
        user.delete()
    return render(request, 'PlantillaMecanico.html', {'mecanico': mecanico,
                                                      'alert': {'icon': 'success',
                                                                'message': 'Mecanico eliminado correctamente '}})

@check_user_roles('ADMIN')
def editar_mecanico(request, id):
    mecanic = Mecanico.objects.get(id=id)
    mecanico = Mecanico.objects.all()
    if request.method == "GET":
        return render(request, 'newMecanic.html', {'mecanic':mecanic})
    else:
        mecanic.nombre = request.POST.get('mecanicnamen')
        mecanic.email = request.POST.get('mail')
        mecanic.fecha_nacimiento = request.POST.get('birth')
        mecanic.dni = request.POST.get('dni')
        mecanic.url = request.POST.get('url')
        mecanic.save()
        return render(request, 'PlantillaMecanico.html', {'mecanico': mecanico,
                                                          'alert': {'icon': 'success',
                                                                    'message': 'Mecanico editado correctamente '}})


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

def login_usuario(request):
    if request.method == "POST":
        NombreUsuario = request.POST.get('nombreusuario')
        contrasenya = request.POST.get('contraseña')
        usuario = authenticate(request, username=NombreUsuario, password=contrasenya)
        if usuario is not None:
            if usuario.rol == Roles.ADMIN:
                login(request, usuario)
                return redirect('jefe')
            elif usuario.rol == Roles.MECANICO:
                login(request, usuario)
                return redirect('mecanico')
            else:
                login(request, usuario)
                return redirect('cliente')
        else:
            return render(request, 'login.html', {"error": "No se ha podido iniciar sesión intentalo de nuevo"})
    return render(request, 'login.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')

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
def area_usuario(request):
    usuario_logeado = request.user
    try:
        cliente = Cliente.objects.get(user=usuario_logeado)
    except Cliente.DoesNotExist:
        cliente = None
    return render(request, 'areaUsuario.html', {'cliente': cliente})

@check_user_roles('ADMIN')
def plantilla_productos(request):
    list_product = Producto.objects.all().order_by('-id')
    return render(request, 'PlantillaProducto.html', {'producto': list_product})

@check_user_roles('ADMIN')
def nuevo_producto(request):
    tipos_producto = Tipo_producto.objects.all()
    marca = MarcaCoche.objects.all()

    if request.method == 'GET':

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
        return render(request, 'newProduct.html', {'tipos_producto': tipos_producto, 'marca': marca,
                                                        'alert': {'icon': 'success',
                                                                  'message': 'Producto añadido correctamente '}})

@check_user_roles('ADMIN')
def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    productos = Producto.objects.all()
    producto.delete()
    return render(request, 'PlantillaProducto.html', {'producto': productos,
                'alert': {'icon': 'success',
                  'message': 'Producto eliminado correctamente '}})

@check_user_roles('ADMIN')
def editar_producto(request, id):
    tipos_producto = Tipo_producto.objects.all()
    productos = Producto.objects.all()
    marca = MarcaCoche.objects.all()
    producto = Producto.objects.get(id=id)
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
        return render(request, 'PlantillaProducto.html', {'producto': productos,
                                                          'alert': {'icon': 'success',
                                                                    'message': 'Producto editado correctamente '}})


@check_user_roles('ADMIN')
def nueva_marca(request):
    if request.method == 'GET':
        return render(request, 'newMarca.html')
    else:
        new = MarcaCoche()
        new.nombre = request.POST.get('nombre')
        new.url = request.POST.get('url')
        new.save()
        return render(request, 'newMarca.html', {
                                                      'alert': {'icon': 'success',
                                                                'message': 'Marca añadida correctamente'}})


@check_user_roles('ADMIN')
def mostrar_marcas(request):
    list_marcas = MarcaCoche.objects.all().order_by('-id')
    return render(request, 'listado_marcas.html', {'marcas': list_marcas})

@check_user_roles('ADMIN')
def eliminar_marca(request, id):
    marca = MarcaCoche.objects.get(id=id)
    marcas = MarcaCoche.objects.all()
    marca.delete()
    return render(request, 'listado_marcas.html', {'marcas': marcas,
        'alert': {'icon': 'success',
                  'message': 'Marca eliminada correctamente'}})

@check_user_roles('ADMIN')
def editar_marca(request, id):
    marca = MarcaCoche.objects.get(id=id)
    marcas = MarcaCoche.objects.all()
    if request.method == "GET":
        return render(request, 'newMarca.html', {'marca':marca})
    else:
        marca.nombre = request.POST.get('nombre')
        marca.url = request.POST.get('url')
        marca.save()
        return render(request, 'listado_marcas.html', {'marcas': marcas,
                                                       'alert': {'icon': 'success',
                                                                 'message': 'Marca editada correctamente'}})

def nuevo_tipo_producto(request):
    list_tipos_productos = Tipo_producto.objects.all().order_by('-id')
    if request.method == 'GET':

       return render(request, 'newTipoProducto.html',{'tipos_productos': list_tipos_productos})
    else:
        new = Tipo_producto()
        new.nombre = request.POST.get('nombre')
        new.save()
        return render(request, 'newTipoProducto.html', {'tipos_productos': list_tipos_productos,
                                                       'alert': {'icon': 'success',
                                                                 'message': 'Categoria añadida correctamente'}})


@check_user_roles('ADMIN')
def eliminar_tipo_producto(request, id):
    tipo_producto = Tipo_producto.objects.get(id=id)
    list_tipos_productos = Tipo_producto.objects.all()
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
        return render(request, 'newTipoProducto.html', {'tipos_productos': list_tipos_productos,
                                                        'alert': {'icon': 'success',
                                                                  'message': 'Categoria editada correctamente'}})

@check_user_roles('ADMIN')
def mostrar_presupuestos(request):
    list_presupuestos = Presupuesto.objects.all().order_by('-id')
    return render(request, 'listado_presupuestos.html', {'presupuesto': list_presupuestos})

@check_user_roles('ADMIN')
def mostrar_citas(request):
    list_citas = Citas.objects.all().order_by('-id')
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

def eliminar_cita(request, id):
    cita = Citas.objects.get(id=id)
    citas = Citas.objects.all()
    cita.delete()
    return render(request, 'listado_citas.html', {'citas': citas,
                                                  'alert': {'icon': 'success',
                                                            'message': 'Cita eliminada correctamente'}})

def asignar_cita_jefe(request, id):
    cita = Citas.objects.get(id=id)
    list_citas = Citas.objects.all().order_by('-id')
    mecanicos = Mecanico.objects.all()
    hora_elegida = request.POST.get('hora')
    fecha = request.POST.get('fecha')
    mecanico_elegido = request.POST.get('mecanico')
    fecha_formateada = cambiar_fecha(fecha).strftime("%Y-%m-%d")

    if Citas.objects.filter(fecha=fecha_formateada,hora=hora_elegida,mecanico=mecanico_elegido).exists():
        return render(request, 'listado_citas.html', {'citas': list_citas, 'mecanicos': mecanicos, 'alert': {'icon': 'error', 'message': 'Cita ya ha sido asignada a ese mecanico en esa fecha y hora'}})
    cita.hora = hora_elegida
    cita.mecanico_id = Mecanico.objects.get(id=request.POST.get('mecanico'))
    cita.estado = EstadoCitas.ACEPTADA
    cita.save()
    return render(request, 'listado_citas.html', {'citas': list_citas, 'mecanicos': mecanicos, 'alert': {'icon': 'success', 'message': 'Cita asignada correctamente'}})


def cambiar_fecha(date_string):
    for fmt in ('%b. %d, %Y', '%b %d, %Y'):
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


@check_user_roles('CLIENTE')
def pedir_cita(request):
    usuario_logeado = request.user
    coches = CocheCliente.objects.filter(usuario=request.user)

    try:
        cliente = Cliente.objects.get(user=usuario_logeado)
    except Cliente.DoesNotExist:
        return render(request, 'areaUsuario.html', {'alert': {'icon': 'error','message': 'Debes de estar verificado para poder pedir una cita'}})

    if request.method == 'GET':
        return render(request, 'newCitaCliente.html', {'coches': coches})
    else:
        try:
            fecha_cita = request.POST.get('fecha')
            cita_mismo_dia = Citas.objects.filter(fecha=fecha_cita, cliente=cliente)
            if cita_mismo_dia.count() >= 2:
                  return render(request, 'newCitaCliente.html', {'coches': coches, 'alert': {'icon': 'error','message': 'No puedes pedir más de dos citas el mismo día'}})
            cita = Citas()
            cita.motivo = request.POST.get('motivo')
            cita.fecha = fecha_cita
            cita.cocheCliente = CocheCliente.objects.get(id=request.POST.get('coche'))
            cita.estado = EstadoCitas.PENDIENTE
            cita.usuario = usuario_logeado
            cita.cliente = cliente
            cita.save()
            return render(request, 'newCitaCliente.html', {'coches': coches, 'alert': {'icon': 'success','message': 'Cita reservada correctamente'}})
        except Exception as e:
            return render(request, 'newCitaCliente.html', {'coches': coches, 'alert': {'icon': 'error','message': 'Error al reservar cita'}})


def vista_citas_cliente(request):
    usuario_logeado = request.user
    try:
        cliente = Cliente.objects.get(user=usuario_logeado)
    except Cliente.DoesNotExist:
         return render(request, 'areaUsuario.html', {'alert': {'icon': 'error','message': 'Debes de estar verificado para poder pedir una cita'}})

    citas = Citas.objects.filter(cliente=cliente).order_by('-id')
    return render(request, 'listado_citasCliente.html', {'citas': citas})

def cancelar_cita(request, id):
    cita = Citas.objects.get(id=id)
    cliente = Cliente.objects.get(user=request.user)
    citalista = Citas.objects.filter(cliente=cliente)
    if cita.estado == EstadoCitas.PENDIENTE:
        cita.delete()
        return render(request, 'listado_citasCliente.html',
                      {'citas': citalista, 'alert': {'icon': 'success', 'message': 'Cita cancelada correctamente'}})

    else:
        cita.estado = EstadoCitas.RECHAZADA
        cita.save()
        return render(request, 'listado_citasCliente.html',{'citas':citalista,'alert': {'icon': 'success', 'message': 'Cita cancelada correctamente'}})

@check_user_roles('CLIENTE')
def mostrar_coches(request):

    usuario_logeado = request.user

    try:
        Cliente.objects.get(user=usuario_logeado)
    except Cliente.DoesNotExist:
        return render(request, 'areaUsuario.html', {'alert': {'icon': 'error','message': 'Debes de estar verificado para poder pedir una cita'}})


    cocheCliente = CocheCliente.objects.all().order_by('-id')
    for coche in cocheCliente:
        if coche.usuario.nombreUsuario != request.user.nombreUsuario:
            cocheCliente = cocheCliente.exclude(id=coche.id)
    return render(request, 'listado_cochesCliente.html', {'coches': cocheCliente})

@check_user_roles('CLIENTE')
def nuevo_coche(request):
    coche = CocheCliente.objects.all()
    usuario_logeado = request.user
    try:
        Cliente.objects.get(user=usuario_logeado)
    except Cliente.DoesNotExist:
        return render(request, 'areaUsuario.html', {'alert': {'icon': 'error','message': 'Debes de estar verificado para poder pedir una cita'}})

    if request.method == 'GET':
        return render(request, 'newCoche.html' ,{'coches': coche})
    else:
        try:

            coche = CocheCliente()
            coche.modelo = request.POST.get('modelo')
            coche.marca = request.POST.get('marca')
            coche.matricula = request.POST.get('matricula')
            coche.KM = request.POST.get('kilometros')
            coche.ITV = request.POST.get('ITV')
            coche.usuario_id = usuario_logeado.id
            coche.save()
            return render(request, 'newCoche.html', {'coches': coche, 'alert': {'icon': 'success', 'message': 'Coche añadido correctamente'}})
        except Exception as e:
            return render(request, 'newCoche.html', {'coches': coche, 'alert': {'icon': 'error', 'message': 'Error al añadir coche'}})

@check_user_roles('CLIENTE')
def eliminar_coche(request,id):
    usuario_logeado = request.user
    coche = CocheCliente.objects.filter(id=id)
    coches = CocheCliente.objects.filter(usuario=usuario_logeado)
    coche.delete()
    return render(request, 'listado_cochesCliente.html', {'coches': coches, 'alert': {'icon': 'success', 'message': 'Coche eliminado correctamente'}})

@check_user_roles('CLIENTE')
def editar_coche(request, id):
    coche = CocheCliente.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'newCoche.html', {'coches':coche})
    else:
        usuario_logeado = request.user
        coches = CocheCliente.objects.filter(usuario=usuario_logeado)
        coche.modelo = request.POST.get('modelo')
        coche.marca = request.POST.get('marca')
        coche.matricula = request.POST.get('matricula')
        coche.KM = request.POST.get('kilometros')
        coche.ITV = request.POST.get('ITV')
        coche.usuario_id = usuario_logeado.id
        coche.save()
        return render(request, 'listado_cochesCliente.html', {'coches': coches ,'alert': {'icon': 'success', 'message': 'Coche editado correctamente'}})

@check_user_roles('CLIENTE')
def recambio_coche(request):
    return render(request,'recambio_coche.html')

@check_user_roles('MECANICO')
def area_mecanico(request):
    return render(request, 'AreaMecanico.html')

def nuevo_presupuesto(request, id):
    cita = Citas.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'newPresupuesto.html', {'cita': cita})
    else:
        new = Presupuesto()
        new.cita = cita
        new.fallos = request.POST.get('fallos')
        new.precio = request.POST.get('precio')
        new.fecha_compra = new.cita.fecha
        new.cliente_id = new.cita.cliente_id
        cita.estado = EstadoCitas.FINALIZADA
        cita.save()
        new.save()
        return redirect('lista_citas_mecanico')


def vista_citas_mecanico(request):
    usuario_logeado = request.user
    mecanico = Mecanico.objects.get(user=usuario_logeado)
    citas = Citas.objects.filter(mecanico=mecanico).order_by('-id')
    for cita in citas:
        if cita.estado == EstadoCitas.FINALIZADA or cita.estado == EstadoCitas.RECHAZADA:
            citas = citas.exclude(id=cita.id)
    return render(request, 'listado_citasMecanico.html', {'citas': citas})

@check_user_roles('MECANICO')
def mostrar_presupuesto_mecanico(request):
    usuario_logeado = request.user
    mecanico = Mecanico.objects.get(user=usuario_logeado)
    presupuestos = Presupuesto.objects.filter(cita__mecanico=mecanico).order_by('-id')
    return render(request, 'listado_presupuestosMecanico.html', {'presupuestos': presupuestos})

def sobre_nosotros(request):
    return render(request, 'contactanos.html')
@check_user_roles('CLIENTE')
def lista_productos_tienda(request):
    query = request.GET.get('q')
    if query:
        productos_list = Producto.objects.filter(nombre__icontains=query)
        paginator = Paginator(productos_list, 6)
        page_number = request.GET.get('page')
        productos = paginator.get_page(page_number)
    else:
        productos_list = Producto.objects.all()
        paginator = Paginator(productos_list, 6)
        page_number = request.GET.get('page')
        productos = paginator.get_page(page_number)
    return render(request, 'tienda.html', {'producto': productos})

@check_user_roles('CLIENTE')
def añadir_al_carrito(request, id):
    productos_list = Producto.objects.all()
    cart = {}
    usuario_logeado = request.user
    try:
        cliente = Cliente.objects.get(user=usuario_logeado)
    except Cliente.DoesNotExist:
        return render(request, 'tienda.html',
                      {'producto': productos_list,
                       'alert': {'icon': 'error', 'message': 'Debes de estar verificado para poder comprar'}})

    query = request.GET.get('q')
    if query:
        productos_list = Producto.objects.filter(nombre__icontains=query)
        paginator = Paginator(productos_list, 6)
        page_number = request.GET.get('page')
        productos = paginator.get_page(page_number)
    else:
        productos_list = Producto.objects.all()
        paginator = Paginator(productos_list, 6)
        page_number = request.GET.get('page')
        productos = paginator.get_page(page_number)

    if "cart" in request.session:
        cart = request.session.get("cart", {})
    if str(id) in cart.keys():
        cart[str(id)] = cart[str(id)] + 1
    else:
        cart[str(id)] = 1
    request.session["cart"] = cart
    return render(request, 'tienda.html', {'producto':productos,'alert': {'icon': 'success', 'message': 'Añadido correctamente'}})


@check_user_roles('CLIENTE')
def mostrar_carrito(request):
    usuario_logeado = request.user
    productos_list = Producto.objects.all()
    try:
        cliente = Cliente.objects.get(user=usuario_logeado)
    except Cliente.DoesNotExist:
        return render(request, 'verificarCliente.html',
                      {'alert': {'icon': 'error', 'message': 'Debes de estar verificado para poder comprar'}})

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
        total = round(total, 2)
    return render(request, 'cart.html', {'cart': cart, 'total': total})

@check_user_roles('CLIENTE')
def eliminar_producto_carrito(request, id):
    if "cart" in request.session:
        cart = request.session.get("cart", {})
        if str(id) in cart.keys():
            del cart[str(id)]
        request.session["cart"] = cart
    return redirect('mostrar_carrito')

@check_user_roles('CLIENTE')
def incrementar_carrito(request, producto_id):
    cart = {}
    if "cart" in request.session:
        cart = request.session.get("cart", {})
    if str(producto_id) in cart.keys():
        cart[str(producto_id)] = cart[str(producto_id)] + 1
    request.session["cart"] = cart
    return redirect('mostrar_carrito')

@check_user_roles('CLIENTE')
def disminuir_carrito(request, producto_id):
    cart = {}
    if "cart" in request.session:
        cart = request.session.get("cart", {})
    if str(producto_id) in cart.keys():
        if cart[str(producto_id)] > 1:
            cart[str(producto_id)] = cart[str(producto_id)] - 1
    request.session["cart"] = cart
    return redirect('mostrar_carrito')

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        mail = request.POST.get('mail')
        direccion = request.POST.get('direccion')
        fecha = request.POST.get('fecha')
        user_id = request.user.id
        nuevo_cliente = Cliente()
        nuevo_cliente.nombre = nombre
        nuevo_cliente.email = mail
        nuevo_cliente.direccion = direccion
        nuevo_cliente.fecha_nacimiento = fecha
        nuevo_cliente.user_id = user_id
        nuevo_cliente.save()
        templete = render_to_string('email_template.html', {'nombre': nombre, 'mail': mail, 'direccion': direccion, 'fecha': fecha})
        mail = EmailMessage(
            'Gracias por contactar con nosotros',
            templete,
            settings.EMAIL_HOST_USER,
            [mail]
        )
        mail.fail_silently = False
        mail.send()
        return redirect('cliente')

def comprar_carrito(request):
    session_cart = {}
    if 'cart' in request.session:
        session_cart = request.session.get('cart', {})
    id_logged_user = request.user.id
    clientes = Cliente.objects.filter(user_id=id_logged_user)
    if len(clientes) != 0:
        cliente = clientes[0]
        pedido = Pedido()
        pedido.codigo = "CO-" + str(int(round(time.time() * 1000)))
        pedido.fecha = datetime.today()
        pedido.cliente = cliente
        pedido.save()
        for k in session_cart.keys():
            linea_pedidos = LineaPedido()
            linea_pedidos.producto = Producto.objects.get(id=k)
            linea_pedidos.cantidad = session_cart.get(k)
            linea_pedidos.precio = linea_pedidos.producto.precio
            linea_pedidos.save()
            pedido.linea_pedidos.add(linea_pedidos)
        request.session.pop('cart')
        return redirect('tienda')
    return redirect('mostrar_carrito')

@check_user_roles('CLIENTE')
def mis_pedidos(request):
    usuario_logueado = Usuario.objects.get(id=request.user.id)
    id_logged_user = request.user.id
    cliente = Cliente.objects.get(user_id=id_logged_user)
    pedidos_cliente = Pedido.objects.filter(cliente=cliente).annotate(coste=Sum(ExpressionWrapper(F('linea_pedidos__cantidad') * F('linea_pedidos__producto__precio'), output_field=FloatField())))
    return render(request, 'mis_pedidos.html', {'pedidos': pedidos_cliente})

def detalles_pedidos(request, id):
    pedido = Pedido.objects.filter(id=id).annotate(coste=Sum(ExpressionWrapper(F('linea_pedidos__cantidad') * F('linea_pedidos__producto__precio'), output_field=FloatField())))
    return render(request, 'detalles_pedido.html', {'pedido': pedido[0]})


@check_user_roles('CLIENTE')
def mis_presupuestos(request):
    usuario_logeado = request.user
    cliente = Cliente.objects.get(user=usuario_logeado)
    presupuestos = Presupuesto.objects.filter(cliente=cliente).order_by('-id')
    return render(request, 'mis_presupuestos.html', {'presupuestos': presupuestos})


@login_required
def datos_cliente(request):
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        return render(request, 'verificarCliente.html', {'alert': {'icon': 'error', 'message': 'Debe verificar su cuenta'}})

    if request.method == 'POST':
        nombre = request.POST['nombre']
        fecha_nacimiento = request.POST['fecha_nacimiento']
        direccion = request.POST['direccion']
        email = request.POST['email']
        # Actualizar los atributos del cliente
        cliente.nombre = nombre
        cliente.fecha_nacimiento = fecha_nacimiento
        cliente.direccion = direccion
        cliente.email = email
        # Guardar el cliente
        cliente.save()
        return render(request, 'areaUsuario.html', {'cliente': cliente, 'alert': {'icon': 'success', 'message': 'Datos actualizados correctamente'}})

    else:
        # Pasar el objeto cliente a la plantilla
        return render(request, 'datos_cliente.html', {'cliente': cliente})

@login_required
def cambiar_contraseña(request):
    cliente = Cliente.objects.get(user=request.user)
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        if not check_password(old_password, request.user.password):
            messages.error(request, 'La contraseña antigua es incorrecta.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Tu contraseña fue actualizada exitosamente!')

            return render(request, 'login.html', {'alert': {'icon': 'success', 'message': 'Debe iniciar sesion nuevamente'}})
    return render(request, 'datos_cliente.html',  {'cliente':cliente,'alert': {'icon': 'error', 'message': 'Su contraseña es incorrecta'}})