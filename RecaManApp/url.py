from django.urls import path
from .views import *

urlpatterns = [
    path('header/', header,name='header'),
    path('citas/', show_citas,name='citas'),
    path('citas/new_cita/', new_cita,name='nueva_cita'),
]