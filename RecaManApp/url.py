from django.urls import path

from .views import *

urlpatterns = [
    path('admin/', admin, name='admin'),
    path('header/', header, name='header'),
    path('footer/', footer, name='footer'),
]