from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.admin import TabularInline
from .models import (
    Tooth, 
    ToothSurface, 
    Odontogram, 
    ToothStatus, 
    DentalCondition, 
    ToothTreatment, 
    DentalDocument
)


class ToothSurfaceInline(TabularInline):
    """Visualización de superficies dentales como inline en dientes"""
    model = ToothSurface
    extra = 0
    fields = ('surface', 'description', 'status')


@admin.register(Tooth)
class ToothAdmin(ModelAdmin):
    """Administración de dientes en el catálogo dental"""
    list_display = ('number', 'name', 'tooth_type', 'position', 'status')
    list_filter = ('tooth_type', 'position', 'status')
    search_fields = ('number', 'name')
    inlines = [ToothSurfaceInline]
    fieldsets = (
        (None, {
            'fields': ('number', 'name', 'status')
        }),
        ('Características', {
            'fields': ('tooth_type', 'position', 'description'),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
        # Guardar creado por y actualizado por
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ToothStatusInline(TabularInline):
    """Visualización de estados de dientes como inline en odontogramas"""
    model = ToothStatus
    extra = 0
    fields = ('tooth', 'tooth_state', 'notes', 'status')
    autocomplete_fields = ['tooth']


class DentalConditionInline(TabularInline):
    """Visualización de condiciones dentales como inline en estados de dientes"""
    model = DentalCondition
    extra = 0
    fields = ('condition_type', 'description', 'surface', 'condition_state', 'status')
    autocomplete_fields = ['surface']


@admin.register(ToothSurface)
class ToothSurfaceAdmin(ModelAdmin):
    """Administración de superficies dentales"""
    list_display = ('tooth', 'surface', 'get_surface_display', 'status')
    list_filter = ('surface', 'status', 'tooth__position')
    search_fields = ('tooth__name', 'tooth__number')
    autocomplete_fields = ['tooth']
    fieldsets = (
        (None, {
            'fields': ('tooth', 'surface', 'status')
        }),
        ('Detalles', {
            'fields': ('description',),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
        # Guardar creado por y actualizado por
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Odontogram)
class OdontogramAdmin(ModelAdmin):
    """Administración de odontogramas"""
    list_display = ('patient', 'dentist', 'status')
    list_filter = ('status',)
    search_fields = ('patient__first_name', 'patient__last_name', 'dentist__username')
    autocomplete_fields = ['patient', 'dentist']
    inlines = [ToothStatusInline]
    fieldsets = (
        (None, {
            'fields': ('patient', 'dentist', 'status')
        }),
        ('Observaciones', {
            'fields': ('general_observations',),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
        # Guardar creado por y actualizado por
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ToothStatus)
class ToothStatusAdmin(ModelAdmin):
    """Administración de estados de dientes"""
    list_display = ('odontogram', 'tooth', 'tooth_state', 'recorded_date', 'status')
    list_filter = ('tooth_state', 'status', 'recorded_date')
    search_fields = ('odontogram__patient__first_name', 'odontogram__patient__last_name', 'tooth__name')
    date_hierarchy = 'recorded_date'
    autocomplete_fields = ['odontogram', 'tooth', 'dentist']
    inlines = [DentalConditionInline]
    fieldsets = (
        (None, {
            'fields': ('odontogram', 'tooth', 'tooth_state', 'status')
        }),
        ('Información adicional', {
            'fields': ('dentist', 'notes'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
        # Guardar creado por y actualizado por
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(DentalCondition)
class DentalConditionAdmin(ModelAdmin):
    """Administración de condiciones dentales"""
    list_display = ('tooth_status', 'condition_type', 'condition_state', 'diagnosis_date', 'status')
    list_filter = ('condition_type', 'condition_state', 'status', 'diagnosis_date')
    search_fields = ('tooth_status__tooth__name', 'tooth_status__odontogram__patient__first_name', 
                   'tooth_status__odontogram__patient__last_name', 'description')
    date_hierarchy = 'diagnosis_date'
    autocomplete_fields = ['tooth_status', 'surface', 'dentist']
    fieldsets = (
        (None, {
            'fields': ('tooth_status', 'condition_type', 'condition_state', 'status')
        }),
        ('Detalles', {
            'fields': ('surface', 'description', 'dentist'),
        })
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
        # Guardar creado por y actualizado por
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ToothTreatment)
class ToothTreatmentAdmin(ModelAdmin):
    """Administración de tratamientos por diente"""
    list_display = ('tooth', 'treatment_performed', 'performed_date', 'treatment_state', 'status')
    list_filter = ('treatment_state', 'status', 'performed_date')
    search_fields = ('tooth__name', 'treatment_performed__treatment__name', 
                   'specific_description', 'specific_materials')
    date_hierarchy = 'performed_date'
    autocomplete_fields = ['treatment_performed', 'tooth', 'surface', 'dental_condition', 'dentist']
    fieldsets = (
        (None, {
            'fields': ('treatment_performed', 'tooth', 'treatment_state', 'status')
        }),
        ('Detalles del tratamiento', {
            'fields': ('surface', 'dental_condition', 'specific_description', 'performed_date')
        }),
        ('Información adicional', {
            'fields': ('dentist', 'specific_materials'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
        # Guardar creado por y actualizado por
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class TeethInline(TabularInline):
    """Visualización de dientes relacionados como inline en documentos dentales"""
    model = DentalDocument.teeth.through
    extra = 0
    autocomplete_fields = ['tooth']


@admin.register(DentalDocument)
class DentalDocumentAdmin(ModelAdmin):
    """Administración de documentos dentales"""
    list_display = ('title', 'document_type', 'patient', 'uploaded_date', 'status')
    list_filter = ('document_type', 'status', 'uploaded_date')
    search_fields = ('title', 'patient__first_name', 'patient__last_name', 'description')
    date_hierarchy = 'uploaded_date'
    autocomplete_fields = ['patient', 'appointment']
    inlines = [TeethInline]
    exclude = ('teeth',)  # Excluir porque se maneja con el inline
    fieldsets = (
        (None, {
            'fields': ('title', 'document_type', 'file', 'status')
        }),
        ('Relaciones', {
            'fields': ('patient', 'appointment')
        }),
        ('Detalles', {
            'fields': ('description',),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
        # Guardar creado por y actualizado por
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)