from django.urls import path
from .views import *

urlpatterns = [
    path('jefe/', area_jefe, name='jefe'),
    path('jefe/plantilla_citas/', mostrar_citas, name='lista_citas'),
    path('jefe/nuevo_mecanico/', nuevo_meacanico, name="añadir_mecanico"),
    path('jefe/plantilla_mecanicos/', plantilla_mecanicos, name="lista_mecanicos"),
    path('jefe/eliminar_mecanico/<int:id>', eliminar_mecanico, name="quitar_mecanico"),
    path('jefe/editar_mecanico/<int:id>', editar_mecanico, name="cambiar_mecanico"),
    path('jefe/nuevo_producto/', nuevo_producto, name='añadir_producto'),
    path('jefe/plantilla_productos/', plantilla_productos, name="lista_productos"),
    path('jefe/eliminar_producto/<int:id>', eliminar_producto, name='quitar_producto'),
    path('jefe/editar_producto/<int:id>', editar_producto, name='cambiar_producto'),
    path('jefe/nuevo_mecanico_automatico/<int:id>', registrar_mecanico_usuario, name='añadir_mecanico_usuario'),
    path('jefe/nueva_marca/', nueva_marca, name='añadir_marca'),
    path('jefe/plantilla_marcas/', mostrar_marcas, name='lista_marcas'),
    path('jefe/eliminar_marca/<int:id>', eliminar_marca, name='quitar_marca'),
    path('jefe/editar_marca/<int:id>', editar_marca, name='cambiar_marca'),
    path('jefe/nuevo_tipo_producto/', nuevo_tipo_producto, name='añadir_tipo_producto'),
    path('jefe/eliminar_tipo_producto/<int:id>', eliminar_tipo_producto, name='quitar_tipo_producto'),
    path('jefe/editar_tipo_producto/<int:id>', editar_tipo_producto, name='cambiar_tipo_producto'),
    path('registrar/', registrar_usuario, name="register"),
    path('login/', login_usuario, name="login"),
    path('verificar/', asignar_Usuario, name="verificar"),
]