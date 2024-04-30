from django.urls import path

from .views import *

urlpatterns = [

    path('jefe/', areaboss),
    path('jefe/newmecanic', new_meacanic, name="newMecanic"),
    path('jefe/plantilla', plantillamecanic, name="plantillaMecanico"),
    path('jefe/eliminarmecanico/<int:id>', delete_mecanic, name="deleteMecanic"),
    path('jefe/editarmecanico/<int:id>', edit_mecanic, name="editMecanic"),
    path('registrar', registrar_user, name="register"),
    path('jefe/anyadirUserMecanic/<int:id>', register_mecanic_user, name="registermecanic"),
    path('login', do_login, name="login"),
    path('jefe/citas/', mostrar_citas, name='citas_jefe'),
]
