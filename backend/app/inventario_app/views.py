from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Producto, EntradaInventario, SalidaInventario
from .forms import FiltroProductoForm, EntradaForm, SalidaForm
from app.proveedores_app.models import Proveedor


# ===========================
# LISTADO DE PRODUCTOS
# ===========================
@login_required
def lista_view(request):
    form = FiltroProductoForm(request.GET or None)
    productos = Producto.objects.select_related('categoria').all()

    if form.is_valid():
        q = form.cleaned_data.get('q') or ''
        estado = form.cleaned_data.get('estado')

        if q:
            productos = productos.filter(
                Q(nombre__icontains=q) |
                Q(descripcion__icontains=q) |
                Q(categoria__nombre__icontains=q)
            )
        if estado == 'ok':
            productos = productos.filter(stock__gt=F('stock_minimo'))
        elif estado == 'low':
            productos = productos.filter(stock__lte=F('stock_minimo'))

    total_productos = productos.count()
    total_valor = productos.aggregate(v=Sum(F('stock') * F('precio_unitario')))['v'] or Decimal('0')

    ctx = {
        'form': form,
        'productos': productos,
        'total_productos': total_productos,
        'total_valor': total_valor,
    }
    return render(request, 'inventario/lista.html', ctx)


# ===========================
# REGISTRAR ENTRADA (actualizado con proveedor)
# ===========================
@login_required
def entrada_view(request):
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.responsable = request.user

            # Relacionar proveedor (si fue seleccionado)
            proveedor_id = request.POST.get('proveedor')
            if proveedor_id:
                entrada.proveedor = Proveedor.objects.get(pk=proveedor_id)

            entrada.save()
            return redirect('inventario:detalle', pk=entrada.producto_id)
    else:
        form = EntradaForm()

    return render(request, 'inventario/entrada_form.html', {
        'form': form,
        'proveedores': proveedores
    })


# ===========================
# REGISTRAR SALIDA
# ===========================
@login_required
def salida_view(request):
    if request.method == 'POST':
        form = SalidaForm(request.POST)
        if form.is_valid():
            salida = form.save(commit=False)
            salida.responsable = request.user
            salida.save()
            return redirect('inventario:detalle', pk=salida.producto_id)
    else:
        form = SalidaForm()
    return render(request, 'inventario/salida_form.html', {'form': form})


# ===========================
# DETALLE DE PRODUCTO
# ===========================
@login_required
def detalle_producto_view(request, pk: int):
    producto = get_object_or_404(Producto, pk=pk)
    entradas = producto.entradainventarios.select_related('proveedor').all()[:10]
    salidas = producto.salidainventarios.all()[:10]
    return render(request, 'inventario/detalle_producto.html', {
        'producto': producto,
        'entradas': entradas,
        'salidas': salidas,
    })


# ===========================
# RESUMEN GLOBAL DE INVENTARIO
# ===========================
@login_required
def resumen_view(request):
    productos = Producto.objects.all()
    total_valor = productos.aggregate(v=Sum(F('stock') * F('precio_unitario')))['v'] or Decimal('0')
    return render(request, 'inventario/resumen.html', {
        'productos': productos,
        'total_valor': total_valor,
        'total_productos': productos.count()
    })
