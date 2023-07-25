"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from laboratorio.views import index, lista_laboratorios, eliminar_laboratorio, actualizar_laboratorio, agregar_laboratorio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('lista_laboratorios/', lista_laboratorios, name='lista_laboratorios'),
    path('eliminar_laboratorio/<int:laboratorio_id>/', eliminar_laboratorio, name='eliminar_laboratorio'),
    path('actualizar_laboratorio/<int:laboratorio_id>/', actualizar_laboratorio, name='actualizar_laboratorio'),
    path('agregar_laboratorio/', agregar_laboratorio, name='agregar_laboratorio'),
]


