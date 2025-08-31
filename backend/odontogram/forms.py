from django import forms
from .models import TeethModel


class TeethForm(forms.ModelForm):
    class Meta:
        model = TeethModel
        fields = ["image", "number", "name"]
