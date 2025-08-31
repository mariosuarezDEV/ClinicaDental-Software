from django.db import models
from core.models import AuditModel
# Create your models here.

TYPE_TEMPORALITY = (
    ("1", "Permanente"),
    ("2", "Temporal"),
)


class TeethModel(AuditModel):
    number = models.IntegerField(verbose_name="Número")
    name = models.CharField(max_length=50, verbose_name="Nombre")
    type_temp = models.CharField(
        max_length=1, choices=TYPE_TEMPORALITY, verbose_name="Tipo de diente"
    )

    def __str__(self):
        return self.name
