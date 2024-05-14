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
    path('jefe/nuevo_tipo_producto/', nuevo_tipo_producto, name='añadir_tipo_producto'),
    path('jefe/eliminar_tipo_producto/<int:id>', eliminar_tipo_producto, name='quitar_tipo_producto'),
    path('jefe/editar_tipo_producto/<int:id>', editar_tipo_producto, name='cambiar_tipo_producto'),
    path('jefe/plantilla_presupuestos/', mostrar_presupuestos, name='lista_presupuestos'),
    path('registrar/', registrar_usuario, name="register"),
    path('login/', login_usuario, name="login"),
    path('verificar/', asignar_Usuario, name="verificar"),
    path('error/', error, name='error'),
    path('cliente/', area_usuario, name='cliente'),
    path('cliente/nueva_cita/', pedir_cita, name='añadir_cita_cliente'),
    path('cliente/plantilla_citas/', vista_citas_cliente, name='lista_citas_cliente'),
    path('cliente/eliminar_cita/<int:id>', eliminar_cita, name='quitar_cita'),
    path('cliente/plantilla_coches/', mostrar_coches, name='lista_coches'),
    path('cliente/nuevo_coche/', nuevo_coche, name='añadir_coche'),
    path('cliente/eliminar_coche/<int:id>', eliminar_coche, name='quitar_coche'),
    path('cliente/editar_coche/<int:id>', editar_coche, name='cambiar_coche'),
    path('sobre_nosotros/', sobre_nosotros, name='sobre_nosotros'),
    path('cliente/recambio_coche/', recambio_coche, name='recambios_coche'),
    path('cerrarsesion/', cerrar_sesion, name="cerrasesion"),
    path('areausuario/', areaUsuario, name="areausuario"),
    path('areausuario/pedir_cita', pedir_cita, name="pedircita"),
    path('areausuario/vista_cita', vistacitacliente, name="vistacitacliente"),
    path('areausuario/vista_cita/quitar_cita/<int:id>', eliminar_cita, name="quitarcita")
]
