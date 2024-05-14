from django.urls import path

from .views import *

urlpatterns = [
    path('jefe/', area_jefe, name='jefe'),
    path('jefe/plantilla_citas/', mostrar_citas, name='lista_citas'),
    path('jefe/nuevo_mecanico/', nuevo_meacanico, name="añadir_mecanico"),
    path('jefe/plantilla_mecanicos/', plantilla_mecanicos, name="lista_mecanicos"),
    path('jefe/eliminar_mecanico/<int:id>', eliminar_mecanico, name="quitar_mecanico"),
    path('jefe/editar_mecanico/<int:id>', editar_mecanico, name="cambiar_mecanico"),
    path('jefe/nuevo_mecanico_automatico/<int:id>', registrar_mecanico_usuario, name='añadir_mecanico_usuario'),
    path('jefe/nuevo_producto/', nuevo_producto, name='añadir_producto'),
    path('jefe/plantilla_productos/', plantilla_productos, name="lista_productos"),
    path('jefe/eliminar_producto/<int:id>', eliminar_producto, name='quitar_producto'),
    path('jefe/editar_producto/<int:id>', editar_producto, name='cambiar_producto'),
    path('jefe/nueva_marca/', nueva_marca, name='añadir_marca'),
    path('jefe/plantilla_marcas/', mostrar_marcas, name='lista_marcas'),
    path('jefe/eliminar_marca/<int:id>', eliminar_marca, name='quitar_marca'),
    path('jefe/editar_marca/<int:id>', editar_marca, name='cambiar_marca'),
    path('jefe/nuevo_tipo_producto/', nuevo_tipo_producto, name='añadir_tipo_producto'),
    path('jefe/eliminar_tipo_producto/<int:id>', eliminar_tipo_producto, name='quitar_tipo_producto'),
    path('jefe/editar_tipo_producto/<int:id>', editar_tipo_producto, name='cambiar_tipo_producto'),
    path('jefe/plantilla_presupuestos/', mostrar_presupuestos, name='lista_presupuestos'),
    path('registrar/', registrar_usuario, name="register"),
    path('login/', login_usuario, name="login"),
    path('verificar/', asignar_Usuario, name="verificar"),
    path('error/', error, name='error'),
    path('areausuario/nueva_cita/', pedir_cita, name='añadir_cita_cliente'),
    path('areausuario/eliminar_cita/<int:id>', eliminar_cita, name='quitar_cita'),
    path('areausuario/plantilla_coches/', mostrar_coches, name='lista_coches'),
    path('areausuario/nuevo_coche/', nuevo_coche, name='añadir_coche'),
    path('areausuario/eliminar_coche/<int:id>', eliminar_coche, name='quitar_coche'),
    path('areausuario/editar_coche/<int:id>', editar_coche, name='cambiar_coche'),
    path('sobre_nosotros/', sobre_nosotros, name='sobre_nosotros'),
    path('areausuario/recambio_coche/', recambio_coche, name='recambios_coche'),
    path('cerrarsesion/', cerrar_sesion, name="cerrasesion"),
    path('areausuario/', areaUsuario, name="areausuario"),
    path('areausuario/nueva_cita/', pedir_cita, name='añadir_cita_cliente'),
    path('areausuario/plantilla_citas/', vista_citas_cliente, name='lista_citas_cliente'),
    path('areausuario/vista_cita', vistacitacliente, name="vistacitacliente"),
    path('areausuario/vista_cita/quitar_cita/<int:id>', eliminar_cita, name="quitarcita")

]
