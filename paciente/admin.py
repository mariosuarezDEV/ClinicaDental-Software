from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from .models import PacienteModel, HistorialMedicoPaciente

@admin.register(PacienteModel)
class PacienteAdmin(ModelAdmin):
    list_display = ("nombre_completo", "fecha_nacimiento", "direccion_completa", "limite_credito", "saldo_actual", "telefono", "email", "status")
    search_fields = ("nombre", "apellido", "telefono", "celular", "email")
    list_filter = ("fecha_nacimiento", "limite_credito")
    list_editable = ("telefono","email", "status")
    ordering = ("nombre", "apellido")
    list_per_page = 10
    list_max_show_all = 100
    date_hierarchy = 'fecha_nacimiento'
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'apellido', 'fecha_nacimiento')
        }),
        ('Dirección', {
            'fields': ('calle', 'numero', 'colonia', 'cp', 'ciudad', 'estado', 'pais')
        }),
        ('Control de crédito', {
            'fields': ('limite_credito', 'saldo_actual')
        }),
        ('Contacto', {
            'fields': ('telefono', 'celular', 'email')
        }),
        # Auditoria
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by', 'status'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
        # Guardar creado por y actualizado por
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(HistorialMedicoPaciente)
class HistorialMedicoPacienteAdmin(ModelAdmin):
    list_display = ("paciente", "blood_type", "last_update", "status")
    search_fields = ("paciente__nombre", "paciente__apellido")
    list_filter = ("blood_type", "last_update")
    list_editable = ("status",)
    ordering = ("paciente__nombre", "paciente__apellido")
    list_per_page = 10
    list_max_show_all = 100
    date_hierarchy = 'last_update'
    fieldsets = (
        ('Información del paciente', {
            'fields': ('paciente',)
        }),
        ('Alergias y condiciones médicas', {
            'fields': ('allergies', 'medical_conditions')
        }),
        ('Medicamentos', {
            'fields': ('current_medications', 'past_medications')
        }),
        ('Tipo de sangre', {
            'fields': ('blood_type',)
        }),
        ('Notas adicionales', {
            'fields': ('additional_notes',)
        }),
        # Auditoria
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    # Guardar creado por y actualizado por
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)