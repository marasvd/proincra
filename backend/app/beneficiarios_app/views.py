from django.shortcuts import render, redirect, get_object_or_404
from .models import Beneficiario
from .forms import BeneficiarioForm
from django.db.models import Q


from django.db.models import OuterRef, Subquery
from app.proyectos_core.models import AvanceProyecto
from app.beneficiarios_app.models import Beneficiario

from django.db.models import Q, OuterRef, Subquery
from app.proyectos_core.models import AvanceProyecto
from app.beneficiarios_app.models import Beneficiario

from django.db import transaction
from django.contrib import messages

from django.shortcuts import render

from .forms import BeneficiarioForm
def lista_beneficiarios(request):
    # Texto de búsqueda (nombre o estado)
    q = request.GET.get('q', '').strip().lower()

    # Subconsulta para obtener el último estado de cada beneficiario
    ultimo_estado = AvanceProyecto.objects.filter(
        beneficiario=OuterRef('pk')
    ).order_by('-fecha', '-id').values('estado')[:1]

    beneficiarios = Beneficiario.objects.all().annotate(
        estado_actual=Subquery(ultimo_estado)
    )

    # Filtrado por texto: coincide con nombre o estado
    if q:
        beneficiarios = beneficiarios.filter(
            Q(nombre__icontains=q) |
            Q(estado_actual__icontains=q)
        )

    return render(request, 'beneficiarios/lista.html', {
        'beneficiarios': beneficiarios,
        'q': q,
    })

def dashboard_principal(request):
    return render(request, 'dashboard/dashboard.html')


from django.shortcuts import render
from django.db.models import OuterRef, Subquery
from app.beneficiarios_app.models import Beneficiario
from app.proyectos_core.models import AvanceProyecto


def crear_beneficiario(request):
    if request.method == 'POST':
        form = BeneficiarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('beneficiarios:lista')
    else:
        form = BeneficiarioForm()
    return render(request, 'beneficiarios/formulario.html', {'form': form})

def detalle_beneficiario(request, id):
    beneficiario = get_object_or_404(Beneficiario, id=id)
    return render(request, 'beneficiarios/detalle.html', {'beneficiario': beneficiario})


@transaction.atomic
def eliminar_beneficiario(request, pk):
    beneficiario = get_object_or_404(Beneficiario, pk=pk)
    
    try:
        beneficiario.delete()  # Django eliminará automáticamente avances y evidencias por cascada
        messages.success(request, "El beneficiario y todos sus registros asociados fueron eliminados correctamente.")
    except Exception as e:
        transaction.set_rollback(True)
        messages.error(request, f"Ocurrió un error al eliminar: {e}")
    
    return redirect('beneficiarios:lista')


@transaction.atomic
def editar_beneficiario(request, pk):
    beneficiario = get_object_or_404(Beneficiario, pk=pk)
    if request.method == 'POST':
        form = BeneficiarioForm(request.POST, instance=beneficiario)
        if form.is_valid():
            form.save()
            return redirect('beneficiarios:detalle', id=beneficiario.id)
    else:
        form = BeneficiarioForm(instance=beneficiario)
    return render(request, 'beneficiarios/editar.html', {'form': form, 'beneficiario': beneficiario})
