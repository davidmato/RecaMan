
from django.urls import path
from .views import *
urlpatterns = [
    path('sobre_nosotros/', sobre_nosotros, name='sobre_nosotros'),
    path('nav/', nav, name='nav'),
    path('footer/', footer, name='footer'),
    path('login/', login, name='login'),
    path('header/', header, name='header'),
    path('home/', home, name='home'),
]