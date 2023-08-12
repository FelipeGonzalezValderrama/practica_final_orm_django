from django.shortcuts import render, redirect, get_object_or_404
from .models import Laboratorio, Producto
from django.db.models import Q
from .forms import LaboratorioForm, ProductoForm
from datetime import datetime

#index
def index(request):
    return render(request, "index.html")

#lista los laboratorios
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
        laboratorio.nombre = request.POST["nombre"]
        laboratorio.ciudad = request.POST["ciudad"]
        laboratorio.pais = request.POST["pais"]
        laboratorio.save()
        return redirect("lista_laboratorios")
    else:
        context = {
            "laboratorio": laboratorio,
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

#view producto y query
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
from datetime import datetime

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






