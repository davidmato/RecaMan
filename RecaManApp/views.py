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
        existe_email = Usuario.objects.filter(email=mail).exists()
        if existe_email:
            errores.append('Ya existe un Usuario con ese email')
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

