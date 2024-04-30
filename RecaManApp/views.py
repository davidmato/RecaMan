from django.contrib.auth import authenticate, login
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
        fecha = request.POST.get('fecha-nacimiento')
        password = request.POST.get('contraseña-registro')
        repeatpassword = request.POST.get('confirmar')

        errores = []

        if password != repeatpassword:
            errores.append('Las contraseñas no coinciden')

        existe_usuario = Usuarios.object.filter(nombreUsuario=NameUsuario).exists()

        if existe_usuario:
            errores.append('Ya existe el nombre de ese usuario')

        existe_email = Usuarios.object.filter(email=mail).exists()

        if existe_email:
            errores.append('Ya existe un Usuario con ese email')

        if len(errores) != 0:
            return render(request, 'register.html', {'errores':errores})

        else:
            user = Usuarios.object.create(nombreUsuario=NameUsuario, password=make_password(password), email=mail)
            user.nombre=name
            user.save()
            return redirect('login')




def register_mecanic_user(request, id):
    mecanic = Mecanico.objects.get(id=id)

    if mecanic.user is None:
        user = Usuarios()
        user.nombre = mecanic.nombre.replace(" ","")
        user.nombreUsuario = mecanic.nombre.replace(" ","")
        user.email = mecanic.email
        user.password = make_password(mecanic.dni)
        user.rol = Roles.MECANICO
        user.save()
        return redirect('login')
    else:
        return redirect('plantillaMecanico')






def do_login(request):
    if request.method == "POST":
        NombreUsuario = request.POST.get('nombreusuario')
        contraseña = request.POST.get('contraseña')

        usuario = authenticate(request, username=NombreUsuario, password=contraseña)

        if usuario is not None:
            login(request, usuario)

            return redirect('newMecanic')
        else:

            return render(request, 'login.html', {"error": "No se ha podido iniciar sesión intentalo de nuevo"})


    return render(request, 'login.html')


def mostrar_citas(request):
    list_citas = Citas.objects.all()
    return render(request, 'listado_citas.html', {'citas': list_citas})