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
from .models import PaymentsModel, FinancingModel

# Formularios
from .forms import (
    AppliedTreatmentsFormStep1,
    InteresRateForm,
    HitchForm,
    FinancingForm,
    PaymentsForm,
)
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
import groq
import markdown2
import os
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)

User = get_user_model()


class FormCalculatorView(LoginRequiredMixin, SessionWizardView):
    template_name = "financing_calculator.html"
    form_list = [
        ("step1", AppliedTreatmentsFormStep1),
        ("step2", InteresRateForm),
        ("step3", HitchForm),
    ]

    def done(self, form_list, **kwargs):
        data = {}

        for form in form_list:
            data.update(form.cleaned_data)
        # Process the final data
        treatment = data["applied"]  # this have the final price
        interest_rate = data[
            "interest_rate"
        ]  # this have a name (yearly) and the rate in %
        hitch = data["hitch"]  # this have the down payment
        if treatment.final_price < 50000:
            messages.error(self.request, "El tratamiento debe ser mayor a $50,000")
            return redirect("dashboard")
        # Prompt Engine
        prompt = f"""
        Genera una cotización en **Markdown** usando únicamente los siguientes datos:

        - Precio total del tratamiento: ${treatment.final_price} MXN
        - Enganche: {hitch}%
        - Financiamiento: {interest_rate.name}
        - Tasa de interés anual: {interest_rate.rate}%

        Requisitos:
        1. No inventes datos adicionales (ej. paciente, fecha, doctor).
        2. Calcula:
        - Monto a financiar = Precio total − Enganche
        - Tasa de interés mensual = Tasa anual ÷ 12
        3. Calcula el **pago mensual fijo (cuota constante)** usando la fórmula de amortización francesa:
        P = M * (r * (1 + r)^n) / ((1 + r)^n – 1)
        Donde:
        - M = monto a financiar
        - r = tasa de interés mensual (en decimal, ej. 4.1667% → 0.041667)
        - n = número de meses según el financiamiento
        4. Genera **una tabla de amortización mensual exacta** con las siguientes columnas:
        - Mes
        - Interés (MXN)
        - Amortización de capital (MXN)
        - Pago mensual (MXN)
        - Saldo restante (MXN)
        Calcula correctamente cada mes para que el saldo final sea cero (o diferencia mínima por redondeo).
        5. Todas las cantidades deben mostrarse en **MXN**, con 2 decimales y separador de miles.
        6. Mantén **el formato exacto**:

        Cotización de Tratamiento  
        Concepto | Valor  
        --- | ---  
        Precio total del tratamiento | $XXXX.XX MXN  
        Enganche ({hitch} %) | $XXXX.XX MXN  
        Monto a financiar | $XXXX.XX MXN  
        Financiamiento | {interest_rate.name}  
        Tasa de interés anual | {interest_rate.rate} %  
        Tasa de interés mensual | XX.XX %  
        Pago mensual (cuota fija) | $XXXX.XX MXN  

        Tabla de amortización mensual  
        Mes | Interés (MXN) | Amortización de capital (MXN) | Pago mensual (MXN) | Saldo restante (MXN)  
        1 | ... | ... | ... | ...  
        2 | ... | ... | ... | ...  
        … | … | … | … | …  

        Nota: El saldo final restante se debe a la redondeación de los valores a dos decimales. El pago mensual se mantiene constante en todos los meses.
        """

        client = groq.Groq(
            api_key=os.getenv("GROQ_API_KEY"),
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="openai/gpt-oss-20b",
            stream=False,
        )
        # print(f"La instrucción fue: {prompt}")
        # print(chat_completion.choices[0].message.content)
        self.request.session["financing_markdown"] = chat_completion.choices[
            0
        ].message.content
        return redirect("financing_result")


class FinancingResultView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "financing.view_financing"
    template_name = "financing_result.html"
    form_class = FinancingForm
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        raw_md = self.request.session.pop("financing_markdown", "")
        # Markdown a HTML
        context["financing_html"] = markdown2.markdown(raw_md, extras=["tables"])
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Financiamiento creado exitosamente")
        return super().form_valid(form)


class PaymentsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "financing.add_payments"
    template_name = "payments_form.html"
    form_class = PaymentsForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Pago registrado exitosamente")
        return super().form_valid(form)


class ListFinancingView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "financing.view_payments"
    template_name = "payments_list.html"
    model = FinancingModel
    context_object_name = "financings"

    def get_queryset(self):
        return list(
            FinancingModel.objects.all().select_related(
                "patient", "treatment", "interest_rate"
            )
        )
