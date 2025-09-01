from django.db import models
from core.models import AuditModel
from treatments.models import AppliedTreatmentsModel
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class InteresRateModel(AuditModel):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
