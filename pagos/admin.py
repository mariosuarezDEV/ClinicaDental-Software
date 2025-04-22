from django.contrib import admin

# Register your models here.
from django.contrib import admin
from unfold.admin import ModelAdmin
from datetime import datetime
from django.db.models import Sum
from django.utils.html import format_html
# Importar - Exportar
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import BilleteraModel, FormasPagoModel, TransaccionesModel

class BilleteraResource(resources.ModelResource):
    class Meta:
        model = BilleteraModel
        fields = ('nombre', 'descripcion', 'get_entradas', 'get_salidas', 'get_balance', 'estatus')
        import_id_fields = ('nombre', 'descripcion', 'get_entradas', 'get_salidas', 'get_balance', 'estatus')
        export_order = ('nombre', 'descripcion', 'get_entradas', 'get_salidas', 'get_balance', 'estatus')

@admin.register(BilleteraModel)
class BilleteraAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = BilleteraResource
    list_display = ('nombre', 'descripcion', 'get_entradas', 'get_salidas', 'get_balance', 'status')
    list_filter = ('status',)
    search_fields = ('nombre', 'descripcion')
    list_editable = ('status',)
    list_per_page = 10
    fieldsets = (
        (
            'Información de la billetera', {
                'fields': ('nombre', 'descripcion')
            }
        ),
        (
            'Auditoría', {
                'fields': ('created_at', 'updated_at', 'created_by', 'updated_by', 'status'),
                "classes": ('collapse',)
            }
        ),
    )

    # Campos de solo lectura
    readonly_fields = ('created_at', 'updated_at',
                       'created_by', 'updated_by', 'status')

    # Acciones
    actions = ['activar', 'desactivar']

    def activar(self, request, queryset):
        queryset.update(status=True)
    activar.short_description = "Activar billeteras seleccionadas"

    def desactivar(self, request, queryset):
        queryset.update(status=False)
    desactivar.short_description = "Desactivar billeteras seleccionadas"
    # Total de entradas en el mes
    def get_entradas(self, obj):
        # Obtener el mes actual
        mes_actual = datetime.now().month
        año_actual = datetime.now().year
        total_entradas = TransaccionesModel.ingresos.filter(
            forma_pago__billetera=obj,
            fecha__month=mes_actual,
            fecha__year=año_actual
        ).aggregate(total=Sum('monto'))['total'] or 0
        return format_html(f'<span style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 10px; font-size: 0.9em;">$ {total_entradas}</span>')
    # Total de salidas en el mes
    def get_salidas(self, obj):
        # Obtener el mes actual
        mes_actual = datetime.now().month
        año_actual = datetime.now().year
        total_salidas = TransaccionesModel.gastos.filter(
            forma_pago__billetera=obj,
            fecha__month=mes_actual,
            fecha__year=año_actual
        ).aggregate(total=Sum('monto'))['total'] or 0
        return format_html(f'<span style="background-color: #F44336; color: white; padding: 5px 10px; border-radius: 10px; font-size: 0.9em;">$ {total_salidas}</span>')
    # Obtener el balance de cuenta
    def get_balance(self, obj):
        total_entradas = TransaccionesModel.ingresos.filter(
            forma_pago__billetera=obj
        ).aggregate(total=Sum('monto'))['total'] or 0
        total_salidas = TransaccionesModel.gastos.filter(
            forma_pago__billetera=obj
        ).aggregate(total=Sum('monto'))['total'] or 0
        balance = total_entradas - total_salidas
        return format_html(f'<span style="background-color: #2196F3; color: white; padding: 5px 10px; border-radius: 10px; font-size: 0.9em;">$ {balance}</span>')
    get_entradas.short_description = 'Entradas del Mes'
    
    get_salidas.short_description = 'Salidas del Mes'
    
    get_balance.short_description = 'Balance del mes'


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        obj.updated_at = datetime.now()
        obj.save()
        super().save_model(request, obj, form, change)


@admin.register(FormasPagoModel)
class FormasPagoAdmin(ModelAdmin):
    list_display = ('nombre', 'descripcion', 'balance_html',
                    'catalogo_sat', 'billetera', 'status')
    list_filter = ('status', 'billetera__nombre')
    search_fields = ('nombre', 'descripcion',
                     'catalogo_sat', 'billetera__nombre')
    list_editable = ('status',)
    list_per_page = 10
    fieldsets = (
        (
            'Información de la forma de pago', {
                'fields': ('nombre', 'descripcion', 'balance', 'catalogo_sat', 'billetera')
            }
        ),
        (
            'Auditoría', {
                'fields': ('created_at', 'updated_at', 'created_by', 'updated_by', 'status'),
                "classes": ('collapse',)
            }
        ),
    )

    # Campos de solo lectura
    readonly_fields = ('created_at', 'updated_at',
                       'created_by', 'updated_by', 'status')

    # Acciones
    actions = ['activar', 'desactivar']

    def activar(self, request, queryset):
        queryset.update(status=True)
    activar.short_description = "Activar formas de pago seleccionadas"

    def desactivar(self, request, queryset):
        queryset.update(status=False)
    desactivar.short_description = "Desactivar formas de pago seleccionadas"
    
    def balance_html(self, obj):
        if obj.balance < 0:
            return format_html(f'<span style="background-color: #F44336; color: white; padding: 5px 10px; border-radius: 10px; font-size: 0.9em;">$ {obj.balance}</span>')
        elif obj.balance == 0:
            return format_html(f'<span style="background-color: #2196F3; color: white; padding: 5px 10px; border-radius: 10px; font-size: 0.9em;">$ {obj.balance}</span>')
        else:
            return format_html(f'<span style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 10px; font-size: 0.9em;">$ {obj.balance}</span>')
    balance_html.short_description = 'Balance'
    balance_html.admin_order_field = 'balance'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        obj.updated_at = datetime.now()
        obj.save()
        super().save_model(request, obj, form, change)

@admin.register(TransaccionesModel)
class TransaccionesAdmin(ModelAdmin):
    list_display = ('fecha', 'forma_pago', 'monto', 'tipo_movimiento_html', 'status')
    list_filter = ('status', 'forma_pago__nombre', 'tipo_movimiento')
    search_fields = ('forma_pago__nombre', 'monto')
    list_editable = ('status',)
    list_per_page = 10
    fieldsets = (
        ('Detalles', {
            'fields': ('fecha', 'forma_pago', 'monto', 'tipo_movimiento', 'concepto')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by', 'status'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    actions = ['activar', 'desactivar']
    
    def activar(self, request, queryset):
        queryset.update(status=True)
    activar.short_description = "Activar transacciones seleccionadas"

    def desactivar(self, request, queryset):
        queryset.update(status=False)
    desactivar.short_description = "Desactivar transacciones seleccionadas"
    
    def tipo_movimiento_html(self, obj):
        if obj.tipo_movimiento == 'E':
            return format_html(f'<span style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 10px; font-size: 0.9em;">Entrada</span>')
        else:
            return format_html(f'<span style="background-color: #F44336; color: white; padding: 5px 10px; border-radius: 10px; font-size: 0.9em;">Salida</span>')
    tipo_movimiento_html.short_description = 'Tipo de movimiento'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        obj.updated_at = datetime.now()
        obj.save()
        super().save_model(request, obj, form, change)