from django import forms
from .models import TreatmentsModel, SpecialtyModel


class CreateTreatmentForm(forms.ModelForm):
    class Meta:
        model = TreatmentsModel
        fields = ["name", "description", "price", "speciality", "specialist"]


class CreateSpecialtyForm(forms.ModelForm):
    class Meta:
        model = SpecialtyModel
        fields = ["name", "description"]
