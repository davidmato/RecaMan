from django.urls import path

from .views import *

urlpatterns = [
    path('jefe/', jefe, name='jefe'),
    path('header/', header, name='header'),
    path('footer/', footer, name='footer'),
    path('jefe/newproduct/', new_product, name='newproduct'),
    path('jefe/plantillaproducto/', plantilla_product, name="vistaproducto"),
    path('jefe/editproduct/<int:id>', edit_product, name='editproduct'),
    path('jefe/deleteproduct/<int:id>', delete_product, name='deleteproduct')
]