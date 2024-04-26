from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from RecaManApp.models import *


# Create your views here.

def areaboss(request):
    return render(request, 'newMecanic.html')



def plantillamecanic(request):
    list_mecanic = Mecanico.objects.all()
    return render(request, 'PlantillaMecanico.html',{'mecanico': list_mecanic})


def new_meacanic(request):

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

        return redirect('/recaman/jefe/plantilla')


def delete_mecanic(request, id):
    mecanic = Mecanico.objects.get(id=id)
    mecanic.delete()
    return redirect('/recaman/jefe/plantilla')


def edit_mecanic(request, id):
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

        return redirect('/recaman/jefe/plantilla')


def registrar_user(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        name = request.POST.get('nombre-registro')
        mail = request.POST.get('email-registro')
        NameUsuario = request.POST.get('nom-usuario')
        dicrection = request.POST.get('register-direccion')
        password = request.POST.get('contraseña-registro')
        repeatpassword = request.POST.get('confirmar')

        errores = []

        if password != repeatpassword:
            errores.append('Las contraseñas no coinciden')

        existe_usuario = Usuario.objects.filter(nombreUsuario=NameUsuario).exists()

        if existe_usuario:
            errores.append('Ya existe el nombre de ese usuario')

        existe_email = Usuario.objects.filter(email=mail).exists()

        if existe_email:
            errores.append('Ya existe un Usuario con ese email')

        if len(errores) != 0:
            return render(request, 'register.html', {'errores':errores})

        else:
            user = Usuario.objects.create(nombreUsuario=NameUsuario, password=make_password(password), email=mail)
            user.direccion=dicrection
            user.nombre=name
            user.save()


            return redirect('plantillaMecanico')




