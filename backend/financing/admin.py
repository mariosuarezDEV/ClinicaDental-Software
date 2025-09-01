from django.contrib import admin
from .models import InteresRateModel, FinancingModel, PaymentsModel
# Register your models here.

admin.site.register(InteresRateModel)

admin.site.register(FinancingModel)

admin.site.register(PaymentsModel)
