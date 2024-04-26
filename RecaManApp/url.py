from django.urls import path
from .views import *

urlpatterns = [
    path('jefe/', area_jefe, name='jefe'),
    path('jefe/citas/', mostrar_citas, name='citas_jefe'),
    path('jefe/nuevo_mecanico/', nuevo_meacanico, name="añadir_mecanico"),
    path('jefe/plantilla/', plantilla_mecanicos, name="lista_mecanicos"),
    path('jefe/eliminar_mecanico/<int:id>', eliminar_mecanico, name="quitar_mecanico"),
    path('jefe/editar_mecanico/<int:id>', editar_mecanico, name="cambiar_mecanico"),
    path('register', registrar_usuario, name="register")
]