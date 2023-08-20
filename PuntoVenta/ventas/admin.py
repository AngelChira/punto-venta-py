from django.contrib import admin
from ventas.models import Cliente, Producto

# Register your models here.



class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre', 'telefono')
    search_fields = ['nombre']
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
#Mostrarlo en el panel de administrador de Django  
admin.site.register(Cliente, ClienteAdmin)    

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'cantidad','costo') #Mostrar
    search_fields = ['descripcion'] #Buscardor
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
#Mostrarlo en el panel de administrador de Django
admin.site.register(Producto, ProductoAdmin)