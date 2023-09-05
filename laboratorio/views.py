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

#view lista laboratorios
def lista_laboratorios(request):
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

#elimina laboratorios
def eliminar_laboratorio(laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    laboratorio.delete()
    return redirect("lista_laboratorios")

#actualiza laboratorios
def actualizar_laboratorio(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    
    if request.method == "POST":
        # Procesar el formulario si se envió una solicitud POST
        form = LaboratorioForm(request.POST, instance=laboratorio)
        if form.is_valid():
            form.save()
            return redirect("lista_laboratorios")
    else:
        # Si es una solicitud GET, simplemente renderiza el formulario con los datos actuales del laboratorio
        form = LaboratorioForm(instance=laboratorio)

    context = {
        "form": form,
        "laboratorio": laboratorio,  # Pasa el objeto laboratorio al contexto
    }
    return render(request, "actualizar_laboratorio.html", context)


#agregar laboratorios
def agregar_laboratorio(request):
    if request.method == "POST":
        form = LaboratorioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_laboratorios")
    else:
        form = LaboratorioForm()

    context = {
        "form": form,
    }
    return render(request, "agregar_laboratorio.html", context)

#view lista producto y query
def lista_productos(request):
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
        producto.diferencia =  producto.p_venta - producto.p_costo

    context = {
        "productos": productos,
    }
    return render(request, "lista_productos.html", context)

#eliminar producto view
def eliminar_producto(producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect("lista_productos")

#agregar productos
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
    else:
        form = ProductoForm()

    laboratorios = Laboratorio.objects.all()  # Obtener todos los laboratorios

    context = {
        "form": form,
        "laboratorios": laboratorios,  # Agregar el queryset de laboratorios al contexto
    }
    return render(request, "agregar_producto.html", context)

#actualizar Producto
def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        producto.nombre = request.POST["nombre"]
        producto.laboratorio = Laboratorio.objects.get(id=request.POST["laboratorio"])
        producto.f_fabricacion = datetime.strptime(request.POST["f_fabricacion"], "%Y-%m-%d").date()
        producto.p_costo = request.POST["p_costo"]
        producto.p_venta = request.POST["p_venta"]
        producto.save()
        return redirect("lista_productos")
    else:
        laboratorios = Laboratorio.objects.all()
        context = {
            "producto": producto,
            "laboratorios": laboratorios,
        }
        return render(request, "actualizar_producto.html", context)


#buscador de search del navbar

def buscar_resultados(request):
    search_query = request.GET.get("q")
    
    # Verificar si la consulta coincide con laboratorio
    laboratorios = Laboratorio.objects.filter(
        Q(nombre__icontains=search_query)
        | Q(ciudad__icontains=search_query)
        | Q(pais__icontains=search_query)
    )

    # Verificar si la consulta coincide con  producto
    productos = Producto.objects.filter(
        Q(nombre__icontains=search_query)
        | Q(f_fabricacion__icontains=search_query)
        | Q(p_costo__icontains=search_query)
        | Q(p_venta__icontains=search_query)
    )

    # Redirigir deacuerdo a el resultado de la búsqueda
    if laboratorios.exists():
        # Si hay coincidencias en laboratorios, redirige a la página de laboratorios
        return redirect(f"/lista_laboratorios/?q={search_query}")
    elif productos.exists():
        # Si hay coincidencias en productos, redirige a la página de productos
        return redirect(f"/lista_productos/?q={search_query}")
    else:
        # Si no se encontraron resultados, puedes mostrar un mensaje o redirigir a una página predeterminada
        return render(request, "no_resultados.html")


#no hay resultados para la busqueda
def no_resultados(request):
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