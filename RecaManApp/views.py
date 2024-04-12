from django.shortcuts import render, redirect
from .models import *
# Create your views here.

def header(request):
    return render(request, 'header.html')
def show_citas(request):
    list_citas = citas.objects.all()
    return render(request, 'citas_jefe.html', {'citas': list_citas})

def new_cita(request):
    if request.method == 'GET':
        lista_coches = CocheCliente.objects.all()
        lista_mecanicos = mecanico.objects.all()
        lista_clientes = Usuario.objects.all()
        return render(request, 'citas_jefe.html', {'coches': lista_coches, 'mecanicos': lista_mecanicos, 'clientes': lista_clientes})
    else:
        new = citas()
        new.fecha = request.POST['fecha']
        new.hora = request.POST['hora']
        new.motivo = request.POST['motivo']
        new.cocheCliente = CocheCliente.objects.get(id=request.POST['coche'])
        new.mecanico = mecanico.objects.get(id=request.POST['mecanico'])
        new.usuario = Usuario.objects.get(id=request.POST['cliente'])
        new.save()

        return redirect('nueva_cita')
