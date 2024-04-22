
from django.contrib import admin
from django.urls import path, include

from RecaManApp.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recaman/', include('RecaManApp.url')),
    path('', home)
]
