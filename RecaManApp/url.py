from django.urls import path
from .views import *

urlpatterns = [
    path('jefe/', area_jefe, name='jefe'),
    path('jefe/citas/', mostrar_citas, name='citas_jefe'),
    path('jefe/nuevo_mecanico/', nuevo_meacanico, name="añadir_mecanico"),
    path('jefe/plantilla_mecaicos/', plantilla_mecanicos, name="lista_mecanicos"),
    path('jefe/eliminar_mecanico/<int:id>', eliminar_mecanico, name="quitar_mecanico"),
    path('jefe/editar_mecanico/<int:id>', editar_mecanico, name="cambiar_mecanico"),
    path('jefe/nuevo_producto/', nuevo_producto, name='añadir_producto'),
    path('jefe/plantilla_productos/', plantilla_productos, name="lista_productos"),
    path('jefe/eliminar_producto/<int:id>', delete_product, name='quitar_producto'),
    path('jefe/editar_producto/<int:id>', editar_producto, name='cambiar_producto'),
    path('registrar', registrar_usuario, name="register"),
]