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
from .forms import (
    CreateTreatmentForm,
    CreateSpecialtyForm,
    TreatmentFormStep1,
    TeethFormStep3,
    DetailsFormStep4,
)
from patients.forms import CreatePacienteForm
from formtools.wizard.views import SessionWizardView

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


class ListSpecialtiesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = SpecialtyModel
    template_name = "specialties_list.html"
    context_object_name = "especialidades"
    permission_required = "treatments.view_specialtymodel"
    paginate_by = 10

    def get_queryset(self):
        return list(SpecialtyModel.objects.all())


class CreateSpecialtyView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SpecialtyModel
    template_name = "specialty_form.html"
    form_class = CreateSpecialtyForm
    success_url = reverse_lazy("lista_especialidades")
    permission_required = "treatments.add_specialtymodel"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Especialidad creada exitosamente.")
        return super().form_valid(form)


class UpdateSpecialtyView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SpecialtyModel
    template_name = "specialty_form.html"
    form_class = CreateSpecialtyForm
    success_url = reverse_lazy("lista_especialidades")
    permission_required = "treatments.change_specialtymodel"
    context_object_name = "especialidad"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Especialidad actualizada exitosamente.")
        return super().form_valid(form)


class DeleteSpecialtyView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = SpecialtyModel
    template_name = "specialty_confirm_delete.html"
    success_url = reverse_lazy("lista_especialidades")
    permission_required = "treatments.delete_specialtymodel"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Especialidad eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)


# Create a Treatment Wizard View
class TreatmentWizardView(
    LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView
):
    permission_required = "treatments.add_appliedtreatmentsmodel"
    form_list = [
        ("step1", TreatmentFormStep1),
        ("step3", TeethFormStep3),
        ("step4", DetailsFormStep4),
    ]
    template_name = "treatment_wizard.html"

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        try:
            applied_treatment = AppliedTreatmentsModel.objects.create(
                treatment=data["treatment"],
                patient=data["patient"],
                apply_date=data["apply_date"],
                final_price=data["final_price"],
                status=data["status"],
                notes=data["notes"],
                created_by=self.request.user,
                updated_by=self.request.user,
            )
            if "teeth" in data:
                applied_treatment.teeth.set(data["teeth"])
            applied_treatment.save()
            messages.success(self.request, "Tratamiento aplicado exitosamente.")
        except Exception as e:
            messages.error(self.request, "Error al aplicar tratamiento.")
            print(e)
            # Optionally log the error
        return redirect("lista_tratamientos")
