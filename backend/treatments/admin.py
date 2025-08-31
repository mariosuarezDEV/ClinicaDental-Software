from django.contrib import admin
from .models import SpecialtyModel, TreatmentsModel, AppliedTreatmentsModel
# Register your models here.

admin.site.register(SpecialtyModel)

admin.site.register(TreatmentsModel)

admin.site.register(AppliedTreatmentsModel)
