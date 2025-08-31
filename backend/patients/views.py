# vistas
from django.views.generic import (
    CreateView,
    UpdateView,
    RedirectView,
    DetailView,
    DeleteView,
    ListView,
    TemplateView,
)

# Modelos

# Formularios
from .forms import CreatePacienteForm

# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Shortcuts
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404

# Otros
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils import timezone
import logging
from django.core.cache import cache
from django.db import connection
import random

logger = logging.getLogger(__name__)

User = get_user_model()


class CreatePatientView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    form_class = CreatePacienteForm
    template_name = "patients_form.html"
    success_url = reverse_lazy("dashboard")
    permission_required = "core.add_user"

    def form_valid(self, form):
        form.instance.type_user = "patient"
        form.instance.is_active = True
        form.instance.username = (
            form.instance.first_name.split(" ")[0]
            + "."
            + form.instance.last_name.split(" ")[0]
            + str(random.randint(1, 100))
        )
        messages.success(self.request, "Paciente creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear paciente.")
        return super().form_invalid(form)


class ListPatientsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = "patients_list.html"
    context_object_name = "pacientes"
    permission_required = "core.view_user"

    def get_queryset(self):
        return list(User.objects.filter(type_user="patient"))


class DeletePatientView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = "patients_confirm_delete.html"
    success_url = reverse_lazy("listar_pacientes")
    permission_required = "core.delete_user"


class UpdatePatientView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = CreatePacienteForm
    template_name = "patients_form.html"
    success_url = reverse_lazy("listar_pacientes")
    permission_required = "core.change_user"

    def form_valid(self, form):
        messages.success(self.request, "Paciente actualizado exitosamente.")
        return super().form_valid(form)
