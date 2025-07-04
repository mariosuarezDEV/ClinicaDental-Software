from django.db import models
from base.models import AuditoriaModel


# Create your models here.

class BilleteraModel(AuditoriaModel):
    nombre = models.CharField(max_length=30, verbose_name="Nombre", null=False, blank=False, help_text="Nombre que agrupa a formas de pago")
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True, help_text="Descripción de la billetera")

    class Meta:
        verbose_name = "Billetera"
        verbose_name_plural = "Billeteras"

    def __str__(self):
        return self.nombre


class FormaPagoModel(AuditoriaModel):
    nombre = models.CharField(max_length=30, verbose_name="Nombre", null=False, blank=False, help_text="Nombre de la forma de pago")
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True, help_text="Descripción de la forma de pago")
    balance = models.DecimalField(null=True, max_digits=10, decimal_places=2, verbose_name="Total en la forma de pago")

    billetera = models.ForeignKey(BilleteraModel, on_delete=models.PROTECT, related_name='formas_pago', verbose_name="Billetera")

    class Meta:
        verbose_name = "Forma de Pago"
        verbose_name_plural = "Formas de Pago"

    def __str__(self):
        return self.nombre


class TransaccionModel(AuditoriaModel):
    forma_pago = models.ForeignKey(FormaPagoModel, on_delete=models.PROTECT, related_name='transacciones', verbose_name="Forma de Pago")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto de la Transacción")
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True, help_text="Descripción de la transacción")
    fecha_transaccion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la Transacción")

    tipo = models.CharField(max_length=20, choices=[('ingreso', 'Ingreso'),('gasto', 'Gasto')], default='ingreso', verbose_name="Tipo de Transacción")

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"

    def __str__(self):
        return f"Transacción de {self.monto} en {self.forma_pago.nombre} el {self.fecha_transaccion.strftime('%Y-%m-%d %H:%M:%S')}"
