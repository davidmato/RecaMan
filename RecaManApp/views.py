from django.shortcuts import render

# Create your views here.
def sobre_nosotros(request):
    return render(request, 'Sobre_nosotros.html')


def nav(request):
    return render(request, 'nav.html')

def footer(request):
    return render(request, 'footer.html')

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
