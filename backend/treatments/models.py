from django.db import models
from core.models import AuditModel
from odontogram.models import TeethModel
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


STATUS_CHOICES = (
    ("CD", "Presupuestado"),
    ("PE", "Pendiente"),
    ("AP", "Aplicado"),
    ("CA", "Cancelado"),
)


class AppliedTreatmentsModel(AuditModel):
    treatment = models.ForeignKey(
        TreatmentsModel, on_delete=models.PROTECT, verbose_name="Tratamiento"
    )
    patient = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Paciente")
    teeth = models.ManyToManyField(TeethModel, verbose_name="Dientes", blank=True)
    apply_date = models.DateField(verbose_name="Fecha de aplicación", auto_now_add=True)
    final_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio final"
    )
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, verbose_name="Estado", default="PE"
    )
    notes = models.TextField(verbose_name="Notas", blank=True, null=True)

    def __str__(self):
        return f"{self.treatment.name} - {self.patient.username} - {self.status}"

    class Meta:
        verbose_name = "Tratamiento aplicado"
        verbose_name_plural = "Tratamientos aplicados"
