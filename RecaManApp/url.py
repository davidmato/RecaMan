from django.urls import path

from .views import *

urlpatterns = [
    path('jefe/', jefe, name='jefe'),
    path('header/', header, name='header'),
    path('footer/', footer, name='footer'),
    path('jefe/newproduct/', new_product, name='newproduct'),
    path('jefe/plantillaproducto', edit_product, name='plantillaproducto')
]