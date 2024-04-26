from django.urls import path
from .views import *

urlpatterns = [
    path('header/', header, name='header'),
    path('citas/', show_citas, name='citas'),
]