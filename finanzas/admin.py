# admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Garantia, Financiamiento, Pago
from .utils import generar_plan_pagos
from django.utils import timezone
from datetime import datetime
from pagos.models import TransaccionesModel
@admin.register(Garantia)
class GarantiaAdmin(ModelAdmin):
    list_display = ('marca_auto', 'modelo_auto', 'año_auto', 'es_valida')
    list_filter = ('marca_auto',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        obj.updated_at = datetime.now()
        obj.save()
        super().save_model(request, obj, form, change)

class PagoInline(TabularInline):
    model = Pago
    extra = 0
    readonly_fields = ('numero_cuota', 'fecha_vencimiento', 'cuota_regular', 'mora', 'created_at', 'updated_at', 'created_by', 'updated_by')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        obj.updated_at = datetime.now()
        obj.save()
        super().save_model(request, obj, form, change)

@admin.register(Financiamiento)
class FinanciamientoAdmin(ModelAdmin):
    list_display = ('cliente', 'monto_tratamiento', 'anticipo', 'saldo_financiar', 'plazo_años', 'tasa_interes')
    search_fields = ('cliente__nombre', 'cliente__apellido')
    list_filter = ('plazo_años',)
    inlines = [PagoInline]
    actions = ['generar_plan_pagos']
    
    def generar_plan_pagos(self, request, queryset):
        for financiamiento in queryset:
            generar_plan_pagos(financiamiento)
        self.message_user(request, f"Plan de pagos generado para {queryset.count()} financiamientos")
    generar_plan_pagos.short_description = "Generar plan de pagos"
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        obj.updated_at = datetime.now()
        obj.save()
        super().save_model(request, obj, form, change)

@admin.register(Pago)
class PagoAdmin(ModelAdmin):
    list_display = ('financiamiento', 'numero_cuota', 'fecha_vencimiento', 
                   'cuota_regular', 'monto_pagado', 'forma_pago', 'esta_atrasado', 'mora')
    list_filter = ('financiamiento', 'fecha_vencimiento', 'forma_pago')
    search_fields = ('financiamiento__cliente__nombre',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', 'transaccion')
    autocomplete_fields = ['forma_pago']
    
    fieldsets = (
        ('Información del pago', {
            'fields': ('financiamiento', 'numero_cuota', 'fecha_vencimiento', 'monto_pagado', 'fecha_pago')
        }),
        ('Método de pago', {
            'fields': ('forma_pago', 'transaccion')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by', 'status'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        obj.updated_at = datetime.now()
        
        # If payment amount and method are provided but no transaction exists, create one
        if obj.monto_pagado and obj.forma_pago and not obj.transaccion:
            transaccion = TransaccionesModel.objects.create(
                fecha=obj.fecha_pago or timezone.now().date(),
                monto=obj.monto_pagado,
                concepto=f"Pago cuota {obj.numero_cuota} - Financiamiento {obj.financiamiento.id}",
                tipo_movimiento="E",  # Entrada de dinero
                forma_pago=obj.forma_pago,
                referencia=f"FINPAGO-{obj.id}" if obj.id else f"FINPAGO-NEW",
                created_by=request.user,
                updated_by=request.user
            )
            obj.transaccion = transaccion
            
        obj.save()
        super().save_model(request, obj, form, change)