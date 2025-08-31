from django.db import models
from core.models import AuditModel
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class SpecialtyModel(AuditModel):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"


class TreatmentsModel(AuditModel):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    duration = models.DurationField(verbose_name="Duración", blank=True, null=True)
    speciality = models.ForeignKey(
        SpecialtyModel, on_delete=models.PROTECT, verbose_name="Especialidad"
    )
    specialist = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Especialista",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tratamiento"
        verbose_name_plural = "Tratamientos"
