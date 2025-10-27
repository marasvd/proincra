from django.shortcuts import render, redirect, get_object_or_404
from .models import Beneficiario
from .forms import BeneficiarioForm

def lista_beneficiarios(request):
    estado = request.GET.get('estado')
    query = request.GET.get('q')
    beneficiarios = Beneficiario.objects.all()

    if estado:
        beneficiarios = beneficiarios.filter(estado=estado)
    if query:
        beneficiarios = beneficiarios.filter(nombre__icontains=query)

    return render(request, 'beneficiarios/lista.html', {'beneficiarios': beneficiarios})

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
