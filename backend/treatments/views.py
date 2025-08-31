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
from .models import SpecialtyModel, TreatmentsModel, AppliedTreatmentsModel

# Formularios
from .forms import CreateTreatmentForm

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

logger = logging.getLogger(__name__)

User = get_user_model()


class ListTreatmentsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TreatmentsModel
    template_name = "treatments_list.html"
    context_object_name = "tratamientos"
    permission_required = "treatments.view_treatmentsmodel"
    paginate_by = 10

    def get_queryset(self):
        return list(
            TreatmentsModel.objects.select_related("speciality", "specialist").all()
        )


class CreateTreatmentView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TreatmentsModel
    template_name = "treatment_form.html"
    form_class = CreateTreatmentForm
    success_url = reverse_lazy("lista_tratamientos")
    permission_required = "treatments.add_treatmentsmodel"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Tratamiento creado exitosamente.")
        return super().form_valid(form)


class UpdateTreatmentView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = TreatmentsModel
    template_name = "treatment_form.html"
    form_class = CreateTreatmentForm
    success_url = reverse_lazy("lista_tratamientos")
    permission_required = "treatments.change_treatmentsmodel"
    context_object_name = "tratamiento"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Tratamiento actualizado exitosamente.")
        return super().form_valid(form)


class DeleteTreatmentView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = TreatmentsModel
    template_name = "treatment_confirm_delete.html"
    success_url = reverse_lazy("lista_tratamientos")
    permission_required = "treatments.delete_treatmentsmodel"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Tratamiento eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)
