from django.shortcuts import render, redirect
from .models import *


def admin(request):
    return render(request, 'admin.html')

def header(request):
    return render(request, 'header.html')

def footer(request):
    return render(request, 'footer.html')

# # Create your views here.
#
# def list_employees(request):
#     list_employees = mecanico.objects.all()
#     return render(request, 'listEmployees.html', {'employees':list_employees})
#
# def new_employee(request):
#     if request.method == 'POST':
#
#         new = mecanico()
#         new.nombre = request.POST.get('nombre')
#         new.email = request.POST.get('email')
#         new.fecha_nacimiento = request.POST.get('fecha_nacimiento')
#         new.dni = request.POST.get('dni')
#         new.cita = request.POST.get('cita')
#         new.url = request.POST.get('url')
#         new.save()
#
#         return redirect('/RecaManApp/new_employee')
#
# def edit_employee(request):
#     employee = mecanico.objects.get(id=request.GET.get('id'))
#     if request.method == 'GET':
#         return render(request, 'new_employee.html', {'employee': employee})
#     else:
#         employee.nombre = request.POST.get['nombre']
#         employee.email = request.POST.get['email']
#         employee.fecha_nacimiento = request.POST.get['fecha_nacimiento']
#         employee.dni = request.POST.get['dni']
#         employee.cita = request.POST.get['cita']
#         employee.url = request.POST.get['url']
#         employee.save()
#
#         employee.clear()
#         return redirect('/RecaManApp/new_employee')
#
# def delete_employee(request):
#     employee = mecanico.objects.get(id=request.GET.get('id'))
#     employee.delete()
#     return redirect('/RecaManApp/new_employee')
#
#
def admin(request):
    return render(request, 'admin.html')

def plantilla_admin(request):
    list_admin = producto.objects.all()
    return render(request, 'admin.html', {'admin': list_admin})

def new_product(request):
    if request.method == 'GET':
        tipos_producto = tipo_producto.objects.all()
        marca = marcaCoche.objects.all()
        return render(request, 'admin.html', {'tipos_producto': tipos_producto, 'marca': marca})
    else:

        new = producto()
        new.nombre = request.POST.get('nombre')
        new.url = request.POST.get('url')
        new.descripcion = request.POST.get('descripcion')
        new.marca = marcaCoche.objects.get(id=request.POST.get('marca'))
        new.tipo_producto = tipo_producto.objects.get(id=request.POST.get('tipos_producto'))
        new.precio = request.POST.get('price')
        new.save()

        return redirect('newproduct')