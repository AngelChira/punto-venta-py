from django import forms
from ventas.models import Cliente, Producto

class AddClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('codigo', 'nombre', 'telefono')
        labels = {
            'codigo': 'Código cliente: ',
            'nombre': 'Nombre cliente: ',
            'telefono': 'Telefono cliente: '
        }

#class ClienteForm(forms.Form):
    #class Meta:

#Formulaio para editar cliente
class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('codigo','nombre','telefono')
        labels = {
            'codigo': 'Código cliente: ',
            'nombre': 'Nombre cliente: ',
            'telefono': 'Teleftono cliente: '
        }
        widgets = {
            'codigo' :forms.TextInput(attrs={'type': 'text', 'id':'codigo_editar'}),
            'nombre' :forms.TextInput(attrs={'id':'nombre_editar'}),
            'telefono' :forms.TextInput(attrs={'id':'telefono_editar'}),
        }
    
#Formulario que se mostrar al usuario
#Campos a guardar
# 'codigo' es el campo de fields y 'Codigo de producto' se muestra en el formulario
class AddProductoForm(forms.ModelForm):
    class Meta:
        model = Producto #Tabla
        fields = ('codigo' ,'descripcion', 'imagen', 'costo', 'precio', 'cantidad') 
        labels = {
            'codigo': 'Codigo Producto: ', 
            'descripcion': 'Descripcion Producto: ',
            'imagen': 'Imagen: ',
            'costo': 'Costo:',
            'precio': 'Precio: ',
            'cantidad': 'Cantidad: ',
        } 
        