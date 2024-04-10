from django.shortcuts import render, redirect

from RecaManApp.models import *


# Create your views here.

def areaboss(request):
    return render(request, 'Area_Admin.html')


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

        return redirect('/recaman/jefe')
