from django.shortcuts import render, redirect
from .models import Cliente, Producto, Egreso, ProductosEgreso
from .forms import AddClienteForm, EditarClienteForm, AddProductoForm
from django.contrib import messages
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from weasyprint.text.fonts import FontConfiguration
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.conf import settings
import os

# Create your views here.

#Vista de venta
def ventas_view(request):
    producto = Producto.objects.all()
    context = {
        'productos' : producto,
    }
    return render(request, 'ventas.html', context)

#Vista de agregar venta
class add_ventas(ListView):
    template_name = 'add_ventas.html'
    model = Egreso

    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    # def get_queryset(self):
    #     return ProductosPreventivo.objects.filter(
    #         preventivo=self.kwargs['id']
    #     )
    
    def post(self, request,*ars, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data,safe=False)


#Vista de Clientes
def clientes_view(request):
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar = EditarClienteForm()
    context = {
        'clientes' : clientes,
        'form_personal' : form_personal,
        'form_editar': form_editar,
    }
    return render(request, 'clientes.html', context)

#Vista para agregar Clientes
def add_cliente_view(request):
    #print("Guardar Cliente")
    if request.POST:
        form = AddClienteForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages(request,"Erro al guardar cliente")
                return redirect('Clientes')
    return redirect('Clientes')

#Vista para editar Clientes
def edit_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_editar'))
        form = EditarClienteForm(
            request.POST,
            request.FILES,
            instance=cliente)
        if form.is_valid():
            form.save()
    return redirect('Clientes')

#Vista de eliminar clientes
def delete_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_eliminar'))
        cliente.delete()           
    return redirect('Clientes')

#Vista de produto
def productos_view(request):
    productos = Producto.objects.all()
    form_producto = AddProductoForm()  
    context = {
        'productos' : productos,
        'form_producto' : form_producto,
    }
    return render(request, 'productos.html', context)

#Vista de agregar producto
def add_producto_view(request):
    #print("Guardar productp")
    if request.POST:
        form = AddProductoForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages(request,"Erro al guardar producto")
                return redirect('Productos')
    return redirect('Productos')

#Vista de pdf
def export_pdf_view(request, id, iva):
    #print(id)
    template = get_template("ticket.html")
    #print(id)
    subtotal = 0 
    iva_suma = 0 

    venta = Egreso.objects.get(pk=float(id))
    datos = ProductosEgreso.objects.filter(egreso=venta)
    for i in datos:
        subtotal = subtotal + float(i.subtotal)
        iva_suma = iva_suma + float(i.iva)

    empresa = "Mi empresa S.A. De C.V"
    context ={
        'num_ticket': id,
        'iva': iva,
        'fecha': venta.fecha_pedido,
        'cliente': venta.cliente.nombre,
        'items': datos, 
        'total': venta.total, 
        'empresa': empresa,
        'comentarios': venta.comentarios,
        'subtotal': subtotal,
        'iva_suma': iva_suma,
    }
    html_template = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; ticket.pdf"
    css_url = os.path.join(settings.BASE_DIR,'index\static\index\css/bootstrap.min.css')
    HTML(string=html_template).write_pdf(target="ticket.pdf", stylesheets=[CSS(css_url)])
   
    font_config = FontConfiguration()
    HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(target=response, font_config=font_config,stylesheets=[CSS(css_url)])

    return response