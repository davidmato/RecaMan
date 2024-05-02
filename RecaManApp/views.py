from django.shortcuts import render, redirect

from RecaManApp.models import *


# Create your views here.
def sobre_nosotros(request):
    return render(request, 'Sobre_nosotros.html')


def nav(request):
    return render(request, 'nav.html')

def footer(request):
    return render(request, 'footer.html')


def login(request):
    return render(request, 'login.html')

def header(request):
    return render(request, 'header.html')

def home(request):
    return render(request, 'home.html')



def areaboss(request):
    return render(request, 'Area_Admin.html')


def plantillamecanic(request):
    list_mecanic = Mecanico.objects.all()
    return render(request, 'PlantillaMecanico.html',{'mecanico': list_mecanic})


def new_meacanic(request):

    if request.method == 'GET':
        return render(request, 'Area_Admin.html')
    else:

        nuevo = Mecanico()
        nuevo.nombre = request.POST.get('mecanicnamen')
        nuevo.email = request.POST.get('mail')
        nuevo.fecha_nacimiento = request.POST.get('birth')
        nuevo.dni = request.POST.get('dni')
        nuevo.url = request.POST.get('url')
        nuevo.save()

        return redirect('/recaman/jefe/plantilla')


def delete_mecanic(request, id):
    mecanic = Mecanico.objects.get(id=id)
    mecanic.delete()
    return redirect('/recaman/jefe/plantilla')


def edit_mecanic(request, id):
    mecanic = Mecanico.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'EditarMecanico.html', {'mecanic': mecanic})
    else:
        mecanic.nombre = request.POST.get('mecanicnamen')
        mecanic.email = request.POST.get('mail')
        mecanic.fecha_nacimiento = request.POST.get('birth')
        mecanic.dni = request.POST.get('dni')
        mecanic.url = request.POST.get('url')
        mecanic.save()
        return redirect('/recaman/jefe/plantilla')


def recambio_coche(request):
    list_mecanic = Mecanico.objects.all()
    list_coches = CocheCliente.objects.all()
    mensajes = [coche.necesita_cambio() for coche in list_coches]
    return render(request, 'PlantillaMecanico.html', {'mecanico': list_mecanic, 'mensajes': mensajes})

def necesita_cambio(self):
    umbral_cambio = 10000  # Define tu umbral aquí
    if self.KM >= umbral_cambio:
        return f"Es necesario realizar un cambio en el coche con matrícula {self.matricula}. Ha recorrido {self.KM} kilómetros."
    else:
        return f"El coche con matrícula {self.matricula} ha recorrido {self.KM} kilómetros. Aún no es necesario realizar un cambio."


# def add_to_cart(request, id):
#     carrito = {}
#
#     #comprobar si hay un carrito en la sesion
#     if 'carrito' in request.session:
#         carrito = request.session.get('carrito', {})
#
#     #comprobar si el prducto esta o no en el carrito
#
#     if str(id) in carrito.keys():
#         carrito[str(id)] = carrito[str(id)] + 1
#     else:
#         carrito[str(id)] = 1
#
#
#     request.session['carrito'] = carrito
#
#     return redirect('/recaman/')
#
#
# def show_cart(request):
#     carrito = {}
#     sessin_carrito = {}
# 
#     total = 0.0
#
#     if 'carrito' in request.session:
#         sessin_carrito = request.session.get('carrito', {})
#
#
#     for key in sessin_carrito.keys():
#         product = Item.objects.get(id=(key))
#         amount = carrito[key]
#         carrito[product] = amount
#
#
#     return render(request, 'Carrito.html', {'carrito': carrito})







