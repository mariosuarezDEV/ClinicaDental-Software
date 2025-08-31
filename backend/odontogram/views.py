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
from .models import TeethModel

# Formularios
from .forms import TeethForm

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


class OdontogramView(TemplateView):
    template_name = "odontogram.html"
    context_object_name = "odontogram"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teeth"] = TeethModel.objects.all().order_by("number")
        return context


class CreateTeethView(CreateView):
    model = TeethModel
    form_class = TeethForm
    template_name = "odontogram_form.html"
    success_url = reverse_lazy("odontograma")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Diente creado exitosamente.")
        return super().form_valid(form)
