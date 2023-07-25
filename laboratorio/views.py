from django.shortcuts import render, redirect, get_object_or_404
from .models import Laboratorio
from django.shortcuts import render
from .models import Laboratorio
from .forms import LaboratorioForm

def index(request):
    return render(request, "index.html")


def lista_laboratorios(request):
    laboratorios = Laboratorio.objects.all()
    context = {
        'laboratorios': laboratorios,
    }
    return render(request, 'laboratorio/lista_laboratorios.html', context)

def eliminar_laboratorio(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    laboratorio.delete()
    return redirect('lista_laboratorios')

def actualizar_laboratorio(request, laboratorio_id):
    laboratorio = get_object_or_404(Laboratorio, id=laboratorio_id)
    if request.method == 'POST':
        laboratorio.nombre = request.POST['nombre']
        laboratorio.ciudad = request.POST['ciudad']
        laboratorio.pais = request.POST['pais']
        laboratorio.save()
        return redirect('lista_laboratorios')
    else:
        context = {
            'laboratorio': laboratorio,
        }
        return render(request, 'laboratorio/actualizar_laboratorio.html', context)
    
    
def agregar_laboratorio(request):
    if request.method == 'POST':
        form = LaboratorioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_laboratorios')
    else:
        form = LaboratorioForm()
    
    context = {
        'form': form,
    }
    return render(request, 'laboratorio/agregar_laboratorio.html', context)


