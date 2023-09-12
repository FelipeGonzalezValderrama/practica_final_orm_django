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
from laboratorio.views import (
    index,
    ListaLaboratoriosView,
    eliminar_laboratorio,
    ActualizarLaboratorioView,
    AgregarLaboratorioView,
    ListaProductosView,
    eliminar_producto,
    AgregarProductoView,
    ActualizarProductoView,
    NoResultadosView,
    BuscarResultadosView,
    LogoutView,
    LoginView,
    RegistroView,
)

urlpatterns = [
    path("", index, name="index"),
    path("lista_laboratorios/", ListaLaboratoriosView.as_view(), name="lista_laboratorios"),
    path("eliminar_laboratorio/<int:laboratorio_id>/",eliminar_laboratorio,name="eliminar_laboratorio",),
    path("actualizar_laboratorio/<int:laboratorio_id>/",ActualizarLaboratorioView.as_view(),name="actualizar_laboratorio",),
    path("agregar_laboratorio/", AgregarLaboratorioView.as_view(), name="agregar_laboratorio"),
    path("lista_productos/", ListaProductosView.as_view(), name="lista_productos"),
    path("eliminar_producto/<int:producto_id>/",eliminar_producto,name="eliminar_producto",),
    path("agregar_producto/", AgregarProductoView.as_view(), name="agregar_producto"),
    path("actualizar_producto/<int:producto_id>/",ActualizarProductoView.as_view(),name="actualizar_producto",),
    path("no_resultados/", NoResultadosView.as_view(), name="no_resultados"),
    path("resultados_busqueda/", BuscarResultadosView.as_view(), name="resultados_busqueda"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registro/", RegistroView.as_view(), name="registro"),
]
