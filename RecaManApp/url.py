from django.urls import path

from .views import *

urlpatterns = [

    path('jefe/', areaboss),
    path('jefe/newmecanic', new_meacanic, name="newMecanic"),
    path('jefe/plantilla', plantillamecanic, name="plantillaMecanico"),
    path('jefe/eliminarmecanico/<int:id>', delete_mecanic, name="deleteMecanic"),
    path('jefe/editarmecanico/<int:id>', edit_mecanic, name="editMecanic"),
    path('registrar', registrar_user, name="register"),
    path('jefe/anyadirUserMecanic/<int:id>', registrar_mecanico_usuario, name="registermecanic"),
    path('login', do_login, name="login"),
    path('jefe/citas/', mostrar_citas, name='citas_jefe'),
    path('verificar', asignar_Usuario, name='verificar'),
    path('areausuario', areaUsuario, name='areausuario'),
    path('pedircita', pedir_cita, name="pedircita"),
    path('jefe/nuevo_producto/', nuevo_producto, name='añadir_producto'),
    path('jefe/plantilla_productos/', plantilla_productos, name="lista_productos"),
    path('jefe/eliminar_producto/<int:id>', eliminar_producto, name='quitar_producto'),
    path('jefe/editar_producto/<int:id>', editar_producto, name='cambiar_producto'),
]
