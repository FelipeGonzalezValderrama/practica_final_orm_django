from django.shortcuts import render, redirect, get_object_or_404
from .models import Laboratorio, Producto
from django.db.models import Q
from .forms import LaboratorioForm, ProductoForm
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistroUsuarioForm 


#index
def index(request):
    return render(request, "index.html")

#lista de laboratorios
class ListaLaboratoriosView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request):
        search_query = request.GET.get("q")
        if search_query:
            laboratorios = Laboratorio.objects.filter(
                Q(nombre__icontains=search_query)
                | Q(ciudad__icontains=search_query)
                | Q(pais__icontains=search_query)
            )
        else:
            laboratorios = Laboratorio.objects.all()

        context = {
            "laboratorios": laboratorios,
        }
        return render(request, "lista_laboratorios.html", context)

    def eliminar_laboratorio(self, laboratorio_id):
        laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
        laboratorio.delete()
        return redirect("lista_laboratorios")

#elimina laboratorios
def eliminar_laboratorio(laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    laboratorio.delete()
    return redirect("lista_laboratorios")


# Actualiza laboratorios
class ActualizarLaboratorioView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request, laboratorio_id):
        laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
        form = LaboratorioForm(instance=laboratorio)
        context = {
            "form": form,
            "laboratorio": laboratorio,
        }
        return render(request, "actualizar_laboratorio.html", context)

    def post(self, request, laboratorio_id):
        laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
        form = LaboratorioForm(request.POST, instance=laboratorio)
        if form.is_valid():
            form.save()
            return redirect("lista_laboratorios")
        context = {
            "form": form,
            "laboratorio": laboratorio,
        }
        return render(request, "actualizar_laboratorio.html", context)


# Agregar laboratorios
class AgregarLaboratorioView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request):
        form = LaboratorioForm()
        context = {
            "form": form,
        }
        return render(request, "agregar_laboratorio.html", context)

    def post(self, request):
        form = LaboratorioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_laboratorios")
        context = {
            "form": form,
        }
        return render(request, "agregar_laboratorio.html", context)

# Lista de productos
class ListaProductosView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request):
        search_query = request.GET.get("q")
        if search_query:
            productos = Producto.objects.filter(
                Q(nombre__icontains=search_query)
                | Q(laboratorio__nombre__icontains=search_query)
                | Q(f_fabricacion__icontains=search_query)
                | Q(p_costo__icontains=search_query)
                | Q(p_venta__icontains=search_query)
            )
        else:
            productos = Producto.objects.all()

        # Calcular la diferencia para cada producto
        for producto in productos:
            producto.diferencia = producto.p_venta - producto.p_costo

        context = {
            "productos": productos,
        }
        return render(request, "lista_productos.html", context)

    def eliminar_producto(self, producto_id):
        producto = get_object_or_404(Producto, id=producto_id)
        producto.delete()
        return redirect("lista_productos")

#eliminar producto view
def eliminar_producto(producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect("lista_productos")

# Agregar productos
class AgregarProductoView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request):
        form = ProductoForm()
        laboratorios = Laboratorio.objects.all()
        context = {
            "form": form,
            "laboratorios": laboratorios,
        }
        return render(request, "agregar_producto.html", context)

    def post(self, request):
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
        laboratorios = Laboratorio.objects.all()
        context = {
            "form": form,
            "laboratorios": laboratorios,
        }
        return render(request, "agregar_producto.html", context)

# Actualizar producto
class ActualizarProductoView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request, producto_id):
        producto = get_object_or_404(Producto, id=producto_id)
        laboratorios = Laboratorio.objects.all()
        context = {
            "producto": producto,
            "laboratorios": laboratorios,
        }
        return render(request, "actualizar_producto.html", context)

    def post(self, request, producto_id):
        producto = get_object_or_404(Producto, id=producto_id)
        producto.nombre = request.POST["nombre"]
        producto.laboratorio = Laboratorio.objects.get(id=request.POST["laboratorio"])
        producto.f_fabricacion = datetime.strptime(request.POST["f_fabricacion"], "%Y-%m-%d").date()
        producto.p_costo = request.POST["p_costo"]
        producto.p_venta = request.POST["p_venta"]
        producto.save()
        return redirect("lista_productos")


# Buscar resultados
class BuscarResultadosView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request):
        search_query = request.GET.get("q")
        
        # Verificar si la consulta coincide con laboratorio
        laboratorios = Laboratorio.objects.filter(
            Q(nombre__icontains=search_query)
            | Q(ciudad__icontains=search_query)
            | Q(pais__icontains=search_query)
        )

        # Verificar si la consulta coincide con producto
        productos = Producto.objects.filter(
            Q(nombre__icontains=search_query)
            | Q(f_fabricacion__icontains=search_query)
            | Q(p_costo__icontains=search_query)
            | Q(p_venta__icontains=search_query)
        )

        # Redirigir de acuerdo a el resultado de la búsqueda
        if laboratorios.exists():
            # Si hay coincidencias en laboratorios, redirige a la página de laboratorios
            return redirect(f"/lista_laboratorios/?q={search_query}")
        elif productos.exists():
            # Si hay coincidencias en productos, redirige a la página de productos
            return redirect(f"/lista_productos/?q={search_query}")
        else:
            # Si no se encontraron resultados, puedes mostrar un mensaje o redirigir a una página predeterminada
            return render(request, "no_resultados.html")


# No hay resultados para la búsqueda
class NoResultadosView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request):
        return render(request, "no_resultados.html")


# Login
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {"login_form": form}
        return render(request, "login.html", context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Iniciaste sesion como: {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalido username o password.")
        else:
            messages.error(request, "Invalido username o password.")

        context = {"login_form": form}
        return render(request, "login.html", context)


#Logout
class LogoutView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request):
        logout(request)
        messages.info(request, "Se ha cerrado la sesión satisfactoriamente.")
        return redirect("/")
    

    #registro
class RegistroView(View):
    def get(self, request):
        form = RegistroUsuarioForm()
        context = {"register_form": form}
        return render(request, "registro.html", context)

    def post(self, request):
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro Exitoso.")
            return redirect("/")
        else:
            messages.error(request, "Registro invalido. Algunos datos ingresados no son correctos")
            context = {"register_form": form}
            return render(request, "registro.html", context)
        
        