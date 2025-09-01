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


class FinancingModel(AuditModel):
    patient = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="financings",
        verbose_name="Paciente",
    )
    treatment = models.ForeignKey(
        AppliedTreatmentsModel, on_delete=models.PROTECT, verbose_name="Tratamiento"
    )
    interest_rate = models.ForeignKey(
        InteresRateModel, on_delete=models.PROTECT, verbose_name="Tasa de Interés"
    )
    down_payment = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Enganche"
    )
    total_financed = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Total Financiado"
    )
    monthly_payment = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Pago Mensual"
    )
    date_payment = models.DateField(verbose_name="Fecha de Pago", null=True, blank=True)

    def __str__(self):
        return f"Financing for {self.patient} - {self.treatment} (ID: {self.id})"


class PaymentsModel(AuditModel):
    financing = models.ForeignKey(
        FinancingModel,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Financiamiento",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    payment_date = models.DateField(verbose_name="Fecha de Pago")

    def __str__(self):
        return f"Payment for {self.financing} - {self.amount}"
