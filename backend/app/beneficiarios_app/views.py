# proyectos_core/views.py
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import HttpResponseForbidden
from gestion_usuarios.models import Modulo
from .models import Beneficiario

def check_perm(user, letter):
    """Helper rápido: devuelve True si user tiene permiso en modulo 'beneficiarios'."""
    if not user.is_authenticated:
        return False
    return user.has_perm_module(Modulo.BENEFICIARIOS, letter)

class BeneficiarioListView(LoginRequiredMixin, ListView):
    model = Beneficiario
    template_name = 'proyectos_core/beneficiario_list.html'
    context_object_name = 'beneficiarios'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if not check_perm(request.user, 'V'):
            return HttpResponseForbidden("No tiene permiso para ver beneficiarios.")
        return super().dispatch(request, *args, **kwargs)


class BeneficiarioDetailView(LoginRequiredMixin, DetailView):
    model = Beneficiario
    template_name = 'proyectos_core/beneficiario_detail.html'
    context_object_name = 'beneficiario'

    def dispatch(self, request, *args, **kwargs):
        if not check_perm(request.user, 'V'):
            return HttpResponseForbidden("No tiene permiso para ver detalles.")
        return super().dispatch(request, *args, **kwargs)


class BeneficiarioCreateView(LoginRequiredMixin, CreateView):
    model = Beneficiario
    template_name = 'proyectos_core/beneficiario_form.html'
    fields = ['nombre_beneficiario', 'documento', 'direccion', 'telefono', 'correo']
    success_url = reverse_lazy('proyectos_core:beneficiario_list')

    def dispatch(self, request, *args, **kwargs):
        if not check_perm(request.user, 'C'):
            return HttpResponseForbidden("No tiene permiso para crear beneficiarios.")
        return super().dispatch(request, *args, **kwargs)


class BeneficiarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Beneficiario
    template_name = 'proyectos_core/beneficiario_form.html'
    fields = ['nombre_beneficiario', 'documento', 'direccion', 'telefono', 'correo']
    success_url = reverse_lazy('proyectos_core:beneficiario_list')

    def dispatch(self, request, *args, **kwargs):
        if not check_perm(request.user, 'E'):
            return HttpResponseForbidden("No tiene permiso para editar beneficiarios.")
        return super().dispatch(request, *args, **kwargs)


class BeneficiarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Beneficiario
    template_name = 'proyectos_core/beneficiario_confirm_delete.html'
    success_url = reverse_lazy('proyectos_core:beneficiario_list')

    def dispatch(self, request, *args, **kwargs):
        if not check_perm(request.user, 'D'):
            return HttpResponseForbidden("No tiene permiso para eliminar beneficiarios.")
        return super().dispatch(request, *args, **kwargs)
