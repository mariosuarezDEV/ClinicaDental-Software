from django.db import models

# Create your models here.
from django.db import models
from django.db import transaction
from django.core.validators import MinValueValidator
from base.models import BaseModel
# Create your models here.


class BilleteraModel(BaseModel):
    nombre = models.CharField(
        max_length=30, verbose_name="Nombre", null=False, blank=False, help_text="Nombre que agrupa a formas de pago")
    descripcion = models.TextField(
        verbose_name="Descripción", null=True, blank=True, help_text="Descripción de la billetera")

    class Meta:
        verbose_name = "Billetera"
        verbose_name_plural = "Billeteras"
        db_table = "billeteras"

    def __str__(self):
        return self.nombre


class FormasPagoModel(BaseModel):
    nombre = models.CharField(
        max_length=30, verbose_name="Nombre", null=False, blank=False, help_text="Nombre de la forma de pago")
    descripcion = models.TextField(
        verbose_name="Descripción", null=True, blank=True, help_text="Descripción de la forma de pago")
    balance = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Balance", null=False, blank=False, help_text="Dinero disponible en la forma de pago", validators=[MinValueValidator(0)])
    catalogo_sat = models.CharField(
        max_length=10, verbose_name="Catalogo SAT", null=True, blank=True, help_text="Código SAT de la forma de pago")
    billetera = models.ForeignKey(
        BilleteraModel, on_delete=models.PROTECT, verbose_name="Billetera", help_text="Billetera a la que pertenece la forma de pago", related_name="formas_pago")

    class Meta:
        verbose_name = "Forma de pago"
        verbose_name_plural = "Formas de pago"
        db_table = "formas_pago"

    def __str__(self):
        return self.nombre

# Manager: Total de ingresos y gastos en una forma de pago


class IngresosManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo_movimiento='E')


class GastosManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo_movimiento='S')

class TransaccionesModel(BaseModel):
    fecha = models.DateField(
        verbose_name="Fecha", null=False, blank=False, help_text="Fecha de la transacción")
    monto = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Monto", null=False, blank=False, help_text="Monto de la transacción", validators=[MinValueValidator(0)])
    concepto = models.CharField(
        max_length=100, verbose_name="Concepto", null=False, blank=False, help_text="Concepto de la transacción")
    tipo_movimiento = models.CharField(
        max_length=10, verbose_name="Tipo de movimiento", null=False, blank=False, help_text="Tipo de movimiento de la transacción", choices=[("E", "Entrada"), ("S", "Salida"), ('EPA', 'Entrada por ajuste'), ('SPA', 'Salida por ajuste')])
    forma_pago = models.ForeignKey(
        FormasPagoModel, on_delete=models.PROTECT, verbose_name="Forma de pago", help_text="Forma de pago de la transacción",
        related_name="transacciones")
    referencia = models.CharField(
        max_length=50, verbose_name="Referencia", null=True, blank=True, help_text="Referencia de la transacción")

    objects = models.Manager()
    ingresos = IngresosManager()
    gastos = GastosManager()
    
    # Transacciones para actualizar el balance de la forma de pago
    @classmethod
    def actualizar_balance(cls, forma_pago, monto, tipo_movimiento):
        print(f"Actualizando balance de {forma_pago} con {monto} {tipo_movimiento}")
        with transaction.atomic():
            # Usar F() para evitar condiciones de carrera
            from django.db.models import F
            
            if tipo_movimiento == 'E':
                forma_pago.balance = F('balance') + monto
            elif tipo_movimiento == 'S':
                # Añadir validación para saldo insuficiente si es necesario
                forma_pago.balance = F('balance') - monto
            else:
                raise ValueError("tipo_movimiento debe ser 'E' o 'S'")
                
            forma_pago.save()
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Actualizar balance de la forma de pago
            self.actualizar_balance(self.forma_pago, self.monto, self.tipo_movimiento)

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        db_table = "transacciones"

    def __str__(self):
        return f'{self.fecha} - {self.concepto} - {self.monto}'