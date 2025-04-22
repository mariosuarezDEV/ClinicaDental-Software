# models.py
from django.db import models
from django.utils import timezone
from paciente.models import PacienteModel
from base.models import BaseModel
from decimal import Decimal
from pagos.models import FormasPagoModel, TransaccionesModel

class Garantia(BaseModel):
    marca_auto = models.CharField(max_length=50)
    modelo_auto = models.CharField(max_length=50)
    año_auto = models.IntegerField()
    
    def __str__(self):
        return f"{self.marca_auto} {self.modelo_auto} ({self.año_auto})"
    
    @property
    def es_valida(self):
        """Verifica que el auto no tenga más de 5 años"""
        return (timezone.now().year - self.año_auto) <= 5

class Financiamiento(BaseModel):
    PLAZO_CHOICES = [
        (1, '1 año'),
        (2, '2 años'),
        (3, '3 años'),
    ]
    
    cliente = models.ForeignKey(PacienteModel, on_delete=models.PROTECT, related_name='financiamientos')
    garantia = models.OneToOneField(Garantia, on_delete=models.CASCADE)
    monto_tratamiento = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField(default=timezone.now)
    plazo_años = models.IntegerField(choices=PLAZO_CHOICES)
    
    def __str__(self):
        return f"Financiamiento de {self.cliente} - ${self.monto_tratamiento}"
    
    @property
    def anticipo(self):
        """Calcula el anticipo (35%)"""
        return self.monto_tratamiento * Decimal('0.35')
    
    @property
    def saldo_financiar(self):
        """Calcula el saldo a financiar"""
        return self.monto_tratamiento - self.anticipo
    
    @property
    def tasa_interes(self):
        """Determina la tasa de interés según el plazo"""
        if self.plazo_años == 1:
            return Decimal('0.50')  # 50% a 1 año
        elif self.plazo_años == 2:
            return Decimal('0.60')  # 60% a 2 años
        elif self.plazo_años == 3:
            return Decimal('0.70')  # 70% a 3 años
        return Decimal('0')
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Verificar monto mínimo
        if self.monto_tratamiento < Decimal('50000'):
            raise ValidationError("El monto mínimo para financiamiento es $50,000")
        
        # Verificar garantía
        if not self.garantia.es_valida:
            raise ValidationError("El auto no puede tener más de 5 años de antigüedad")
    
    def calcular_cuota_mensual(self, num_cuota=1):
        """Calcula la cuota mensual con ajuste de inflación"""
        # Asegurarnos que num_cuota no sea None y sea un entero
        if num_cuota is None:
            num_cuota = 1
        
        # Verificar que el plazo_años no sea None
        if self.plazo_años is None:
            return Decimal('0')
            
        monto_total = self.saldo_financiar * (Decimal('1') + self.tasa_interes)
        inflacion_anual = Decimal('0.05')  # 5% anual
        
        # Calcular ajuste por inflación si aplica
        año_actual = (num_cuota - 1) // 12
        if año_actual > 0:
            factor_inflacion = (Decimal('1') + inflacion_anual) ** año_actual
            monto_ajustado = monto_total * factor_inflacion
        else:
            monto_ajustado = monto_total
        
        # Calcular cuota mensual base
        cuotas_totales = self.plazo_años * 12
        cuotas_restantes = cuotas_totales - (num_cuota - 1)
        
        if cuotas_restantes <= 0:
            return Decimal('0')
            
        return monto_ajustado / cuotas_restantes

class Pago(BaseModel):
    financiamiento = models.ForeignKey(Financiamiento, on_delete=models.CASCADE, related_name='pagos')
    numero_cuota = models.IntegerField()
    fecha_vencimiento = models.DateField()
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_pago = models.DateField(null=True, blank=True)
    # New fields:
    forma_pago = models.ForeignKey(FormasPagoModel, on_delete=models.PROTECT, 
                                  null=True, blank=True, 
                                  related_name='financiamiento_pagos', 
                                  verbose_name="Forma de pago")
    transaccion = models.OneToOneField(TransaccionesModel, on_delete=models.SET_NULL, 
                                     null=True, blank=True, 
                                     related_name='financiamiento_pago', 
                                     verbose_name="Transacción")
    
    def __str__(self):
        return f"Pago {self.numero_cuota} de {self.financiamiento}"
    
    @property
    def cuota_regular(self):
        """Obtiene el monto de la cuota regular"""
        return self.financiamiento.calcular_cuota_mensual(self.numero_cuota)
    
    @property
    def esta_atrasado(self):
        from django.utils import timezone
        # Only compare if fecha_vencimiento is not None
        if self.fecha_vencimiento is None:
            return False  # or True, depending on your business logic
        return timezone.now().date() > self.fecha_vencimiento
    
    @property
    def mora(self):
        """Calcula la mora si el pago está atrasado (10% mensual sobre saldo)"""
        if self.esta_atrasado:
            return self.financiamiento.saldo_financiar * Decimal('0.10')
        return Decimal('0')