# utils.py
from .models import Pago
from django.utils import timezone
from pagos.models import TransaccionesModel

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

def registrar_pago(pago, monto, fecha=None, forma_pago=None):
    """Registra un pago realizado y genera la transacción correspondiente"""
    from django.utils import timezone
    
    if not fecha:
        fecha = timezone.now().date()
    
    pago.monto_pagado = monto
    pago.fecha_pago = fecha
    pago.forma_pago = forma_pago
    
    # Crear transacción si se proporcionó forma de pago
    if forma_pago:
        # Crear la transacción
        transaccion = TransaccionesModel.objects.create(
            fecha=fecha,
            monto=monto,
            concepto=f"Pago cuota {pago.numero_cuota} - Financiamiento {pago.financiamiento.id}",
            tipo_movimiento="E",  # Entrada de dinero
            forma_pago=forma_pago,
            referencia=f"FINPAGO-{pago.id}",
            created_by=pago.created_by,
            updated_by=pago.updated_by
        )
        # Asociar transacción con el pago
        pago.transaccion = transaccion
    
    pago.save()
    
    return {
        'pago': pago,
        'mora_aplicada': pago.mora if fecha > pago.fecha_vencimiento else 0
    }