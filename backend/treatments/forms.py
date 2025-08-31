from django import forms
from .models import TreatmentsModel


class CreateTreatmentForm(forms.ModelForm):
    class Meta:
        model = TreatmentsModel
        fields = ["name", "description", "price", "speciality", "specialist"]
