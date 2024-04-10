from django.shortcuts import render

# Create your views here.
def sobre_nosotros(request):
    return render(request, 'Sobre_nosotros.html')


def nav(request):
    return render(request, 'nav.html')

def footer(request):
    return render(request, 'footer.html')