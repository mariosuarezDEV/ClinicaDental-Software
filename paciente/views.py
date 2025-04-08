# Django
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
# Vistas
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from formtools.wizard.views import SessionWizardView
# Forms
from .forms import PacienteBasicForm, PacienteDireccionForm, PacienteContactoForm, PacienteCreditoForm
# Models
from .models import PacienteModel
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PacienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Vista para listar pacientes"""
    model = PacienteModel
    template_name = 'pacientes.html'
    context_object_name = 'pacientes'
    permission_required = 'paciente.view_pacientemodel'

class PacienteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista para ver los detalles de un paciente"""
    model = PacienteModel
    template_name = 'paciente_detail.html'
    context_object_name = 'paciente'
    permission_required = 'paciente.view_pacientemodel'
    
class PacienteWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    """Vista para el proceso de registro de pacientes"""
    permission_required = 'paciente.add_pacientemodel'
    template_name = 'paciente_wizard_form.html'
    form_list = [
        ('basic', PacienteBasicForm),
        ('direccion', PacienteDireccionForm),
        ('contacto', PacienteContactoForm),
        ('credito', PacienteCreditoForm),
    ]
    
    def done(self, form_list, **kwargs):
        """Método que se llama al finalizar el wizard"""
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)
        # Añadir los campos created_by y updated_by al diccionario form_data
        form_data['created_by'] = self.request.user
        form_data['updated_by'] = self.request.user
        PacienteModel.objects.create(**form_data)
        messages.success(self.request, 'Paciente registrado exitosamente.')
        return HttpResponseRedirect(reverse_lazy('paciente_list'))
