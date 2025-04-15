from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import TreatmentCategory, Treatment, TreatmentPerformed

@admin.register(TreatmentCategory)
class TreatmentCategoryAdmin(ModelAdmin):
    list_display = ('name', 'description', 'color_code', 'status')
    search_fields = ('name', 'description')
    list_filter = ('status',)
    list_editable = ('color_code', 'status')
    ordering = ('name',)
    list_per_page = 10
    
    fieldsets = (
        ('Información de la categoría', {
            'fields': ('name', 'description', 'color_code')
        }),
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

@admin.register(Treatment)
class TreatmentAdmin(ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'estimated_duration', 'requires_laboratory', 'status')
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('category', 'requires_laboratory', 'status')
    list_editable = ('base_price', 'estimated_duration', 'status')
    ordering = ('category', 'name')
    list_per_page = 10
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'description', 'category')
        }),
        ('Detalles económicos', {
            'fields': ('base_price', 'requires_laboratory', 'laboratory_price')
        }),
        ('Detalles operativos', {
            'fields': ('estimated_duration', 'notes')
        }),
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

@admin.register(TreatmentPerformed)
class TreatmentPerformedAdmin(ModelAdmin):
    list_display = ('treatment', 'appointment', 'dentist', 'applied_price', 'status', 'start_datetime', 'end_datetime')
    search_fields = ('treatment__name', 'dentist__username', 'appointment__id', 'notes')
    list_filter = ('status', 'dentist', 'start_datetime')
    list_editable = ('status',)
    ordering = ('-start_datetime',)
    list_per_page = 10
    date_hierarchy = 'start_datetime'
    
    fieldsets = (
        ('Información básica', {
            'fields': ('treatment', 'appointment', 'dentist')
        }),
        ('Detalles del procedimiento', {
            'fields': ('applied_price', 'start_datetime', 'end_datetime', 'status')
        }),
        ('Notas adicionales', {
            'fields': ('notes',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', 'duration_minutes')
    
    # Guardar creado por y actualizado por
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        
    # Añadir campo calculado para la duración
    def duration_minutes(self, obj):
        return obj.duration_minutes
    duration_minutes.short_description = "Duración (minutos)"