from django.shortcuts import render, redirect
from .models import *
# Create your views here.

def header(request):
    return render(request, 'header.html')
def show_citas(request):
    list_citas = citas.objects.all()
    return render(request, 'listado_citas.html', {'citas': list_citas})


