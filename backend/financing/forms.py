from django import forms
from treatments.models import AppliedTreatmentsModel
from .models import InteresRateModel


# Form steps
class AppliedTreatmentsFormStep1(forms.Form):
    applied = forms.ModelChoiceField(
        queryset=AppliedTreatmentsModel.objects.filter(status="CD").select_related(
            "treatment", "patient"
        ),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Tratamiento aplicado",
    )


class InteresRateForm(forms.Form):
    interest_rate = forms.ModelChoiceField(
        queryset=InteresRateModel.objects.filter(active=True).order_by("rate"),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Tasa de interés anual",
    )


class HitchForm(forms.Form):
    hitch = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Enganche",
    )
