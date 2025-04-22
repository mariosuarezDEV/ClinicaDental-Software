# utils.py
from .models import Pago

def generar_plan_pagos(financiamiento):
    """Genera el plan de pagos para un financiamiento"""
    # Eliminar pagos anteriores si existen
    Pago.objects.filter(financiamiento=financiamiento).delete()
    
    fecha_actual = financiamiento.fecha_inicio
    total_cuotas = financiamiento.plazo_años * 12
    
    # Crear cada cuota mensual
    for i in range(1, total_cuotas + 1):
        Pago.objects.create(
            financiamiento=financiamiento,
            numero_cuota=i,
            fecha_vencimiento=fecha_actual
        )
        # Avanzar al siguiente mes
        fecha_actual = fecha_actual.replace(
            month=fecha_actual.month % 12 + 1,
            year=fecha_actual.year + (1 if fecha_actual.month == 12 else 0)
        )

def registrar_pago(pago, monto, fecha=None):
    """Registra un pago realizado"""
    from django.utils import timezone
    
    if not fecha:
        fecha = timezone.now().date()
    
    pago.monto_pagado = monto
    pago.fecha_pago = fecha
    pago.save()
    
    return {
        'pago': pago,
        'mora_aplicada': pago.mora if fecha > pago.fecha_vencimiento else 0
    }