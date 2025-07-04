from django.contrib import admin

# Register your models here.
from .models import CategoriaTratamientoModel, TratamientoModel, TratamientoPacienteModel

admin.site.register(CategoriaTratamientoModel)
admin.site.register(TratamientoModel)
admin.site.register(TratamientoPacienteModel)