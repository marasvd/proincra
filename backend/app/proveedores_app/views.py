from django.shortcuts import render, get_object_or_404, redirect
from .models import Proveedor

def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/lista.html', {'proveedores': proveedores})

def crear_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        nit = request.POST['nit']
        contacto = request.POST['contacto']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        direccion = request.POST['direccion']
        tipo_producto = request.POST['tipo_producto']
        Proveedor.objects.create(
            nombre=nombre,
            nit=nit,
            contacto=contacto,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
            tipo_producto=tipo_producto
        )
        return redirect('proveedores:lista')
    return render(request, 'proveedores/crear.html')

def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.nombre = request.POST['nombre']
        proveedor.nit = request.POST['nit']
        proveedor.contacto = request.POST['contacto']
        proveedor.telefono = request.POST['telefono']
        proveedor.correo = request.POST['correo']
        proveedor.direccion = request.POST['direccion']
        proveedor.tipo_producto = request.POST['tipo_producto']
        proveedor.save()
        return redirect('proveedores:lista')
    return render(request, 'proveedores/editar.html', {'proveedor': proveedor})

def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    proveedor.delete()
    return redirect('proveedores:lista')

def detalle_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    return render(request, 'proveedores/detalle.html', {'proveedor': proveedor})
