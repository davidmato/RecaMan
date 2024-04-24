from django.urls import path

from .views import *

urlpatterns = [

    path('jefe/', areaboss),
    path('jefe/newmecanic', new_meacanic, name="newMecanic"),
    path('jefe/plantilla', plantillamecanic, name="plantillaMecanico"),
    path('jefe/delete_mecanic/<int:id>', delete_mecanic, name="deleteMecanic"),
    path('jefe/edit_mecanic/<int:id>', edit_mecanic, name="editMecanic"),
    path('login', login, name="login")
]
