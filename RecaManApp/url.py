from django.urls import path

from .views import *

urlpatterns = [

    path('jefe/', areaboss),
    path('jefe/newmecanic', new_meacanic, name="newMecanic"),
    path('jefe/plantilla', plantillamecanic, name="plantillaMecanico")
]
