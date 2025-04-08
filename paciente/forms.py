from django import forms
from .models import PacienteModel
from crispy_forms.helper import FormHelper

class PacienteBasicForm(forms.ModelForm):
    class Meta:
        model = PacienteModel
        fields = ['nombre', 'apellido', 'fecha_nacimiento']
        # Fecha de nacimiento como un campo de tipo DateField
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class PacienteDireccionForm(forms.ModelForm):
    class Meta:
        model = PacienteModel
        fields = ['calle', 'numero', 'colonia', 'cp', 'ciudad', 'estado', 'pais']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class PacienteCreditoForm(forms.ModelForm):
    class Meta:
        model = PacienteModel
        fields = ['limite_credito', 'saldo_actual']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class PacienteContactoForm(forms.ModelForm):
    class Meta:
        model = PacienteModel
        fields = ['telefono', 'celular', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False