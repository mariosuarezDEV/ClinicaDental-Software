from django.contrib import admin

# Register your models here.
from .models import FacturaModel, FinanciamientoConfigModel

admin.site.register(FacturaModel)
admin.site.register(FinanciamientoConfigModel)