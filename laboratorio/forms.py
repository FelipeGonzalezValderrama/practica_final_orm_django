from django import forms
from .models import Laboratorio, Producto

#form Laboratorio
class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ['nombre', 'ciudad', 'pais']


#form Producto
class ProductoForm(forms.ModelForm):
    laboratorio = forms.ModelChoiceField(queryset=Laboratorio.objects.all(), empty_label="Seleccione un laboratorio")

    class Meta:
        model = Producto
        fields = ['nombre', 'laboratorio', 'f_fabricacion', 'p_costo', 'p_venta']
        widgets = {
            'f_fabricacion': forms.DateInput(attrs={'type': 'date'}),
        }
        input_formats = ['%Y-%m-%d']
