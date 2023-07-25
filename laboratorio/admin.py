from django.contrib import admin
from .models import Laboratorio, DirectorGeneral, Producto

class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ciudad', 'pais',) # campos visualizados en django admin
    list_editable = ('nombre', 'ciudad', 'pais',) # campos modificables en django admin

class DirectorGeneralAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'laboratorio', 'especialidad',)
    list_editable = ('nombre', 'laboratorio', 'especialidad',)  

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'laboratorio', 'f_fabricacion', 'p_costo', 'p_venta',)
    list_editable = ('nombre', 'laboratorio', 'f_fabricacion', 'p_costo', 'p_venta',)  

admin.site.register(Laboratorio, LaboratorioAdmin)
admin.site.register(DirectorGeneral, DirectorGeneralAdmin)
admin.site.register(Producto, ProductoAdmin)
