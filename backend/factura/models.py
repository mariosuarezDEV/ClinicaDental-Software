from django.db import models
from base.models import AuditoriaModel
from tratamiento.models import TratamientoPacienteModel
from pago.models import FormaPagoModel
# Create your models here.

class FacturaModel(AuditoriaModel):
    tratamiento = models.ForeignKey(TratamientoPacienteModel, on_delete=models.PROTECT, related_name='facturas', verbose_name="Tratamiento")
    forma_pago = models.ForeignKey(FormaPagoModel, on_delete=models.PROTECT, related_name='facturas', verbose_name="Forma de Pago")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Total") # Pasar esto a la transacción como ingreso
    fecha_emision = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Emisión")
    # tipo (contado - credito)
    tipo = models.CharField(max_length=20, choices=[('contado', 'Contado'), ('credito', 'Crédito')], default='contado', verbose_name="Tipo de Factura")
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    def __str__(self):
        return f"Factura #{self.id} - {self.tratamiento.paciente.nombre} - {self.monto_total}"

class FinanciamientoConfigModel(AuditoriaModel):
    nombre = models.CharField(max_length=50, verbose_name="Nombre", null=False, blank=False, help_text="Nombre del financiamiento")
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True, help_text="Descripción del financiamiento")
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Tasa de Interés (%)", default=0.0)
    plazo_meses = models.PositiveIntegerField(verbose_name="Plazo (meses)", default=12)

    class Meta:
        verbose_name = "Configuración de Financiamiento"
        verbose_name_plural = "Configuraciones de Financiamiento"

    def __str__(self):
        return self.nombre

class GarantiaModel(AuditoriaModel):
    pass

class CreditoModel(AuditoriaModel):
    pass