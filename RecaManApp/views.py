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