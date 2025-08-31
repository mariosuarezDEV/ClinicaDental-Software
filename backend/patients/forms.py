from django import forms
from django.contrib.auth import get_user_model

user = get_user_model()


class CreatePacienteForm(forms.ModelForm):
    class Meta:
        model = user
        fields = [
            "first_name",
            "last_name",
            "phone",
            "date_birth",
            "address",
        ]
        widgets = {
            "date_birth": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }
