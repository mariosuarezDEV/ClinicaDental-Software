from django import forms
from .models import TreatmentsModel, SpecialtyModel, AppliedTreatmentsModel
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateTreatmentForm(forms.ModelForm):
    specialist = forms.ModelChoiceField(
        queryset=User.objects.filter(type_user="doctor")
    )

    class Meta:
        model = TreatmentsModel
        fields = ["name", "description", "price", "speciality", "specialist"]


class CreateSpecialtyForm(forms.ModelForm):
    class Meta:
        model = SpecialtyModel
        fields = ["name", "description"]


# Forms Steps
class TreatmentFormStep1(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=User.objects.filter(type_user="patient"))

    class Meta:
        model = AppliedTreatmentsModel
        fields = ["treatment", "patient"]


class TeethFormStep3(forms.ModelForm):
    class Meta:
        model = AppliedTreatmentsModel
        fields = ["teeth"]
        widgets = {
            "teeth": forms.CheckboxSelectMultiple(attrs={"type": "checkbox"}),
        }


class DetailsFormStep4(forms.ModelForm):
    class Meta:
        model = AppliedTreatmentsModel
        fields = ["apply_date", "notes", "status", "final_price"]
        widgets = {
            "apply_date": forms.DateInput(attrs={"type": "date"}),
        }
