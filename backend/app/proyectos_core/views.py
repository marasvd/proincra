from django.shortcuts import render, get_object_or_404, redirect
from .models import AvanceProyecto, Evidencia
from app.beneficiarios_app.models import Beneficiario
from django.contrib.auth.decorators import login_required

def lista_avances(request):
    avances = AvanceProyecto.objects.select_related('beneficiario').all()
    return render(request, 'proyectos_core/lista.html', {'avances': avances})

@login_required
def crear_avance(request):
    beneficiarios = Beneficiario.objects.all()
    if request.method == 'POST':
        beneficiario_id = request.POST.get('beneficiario')
        porcentaje = request.POST.get('porcentaje_avance')
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado')

        beneficiario = get_object_or_404(Beneficiario, id=beneficiario_id)
        AvanceProyecto.objects.create(
            beneficiario=beneficiario,
            tecnico=request.user,
            porcentaje_avance=porcentaje,
            descripcion=descripcion,
            estado=estado
        )
        return redirect('proyectos_core:lista')

    return render(request, 'proyectos_core/crear.html', {'beneficiarios': beneficiarios})

def detalle_avance(request, id):
    avance = get_object_or_404(AvanceProyecto, id=id)
    evidencias = Evidencia.objects.filter(avance=avance)
    return render(request, 'proyectos_core/detalle.html', {'avance': avance, 'evidencias': evidencias})
