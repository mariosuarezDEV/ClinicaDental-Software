from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display = ('patient', 'dentist', 'scheduled_datetime', 'end_datetime', 'status_appointment', 'get_duration_minutes')
    search_fields = ('patient__nombre', 'patient__apellido', 'dentist__username', 'dentist__first_name', 'dentist__last_name', 'reason')
    list_filter = ('status_appointment', 'scheduled_datetime', 'dentist')
    list_editable = ('status_appointment',)
    ordering = ('-scheduled_datetime',)
    list_per_page = 10
    list_max_show_all = 100
    date_hierarchy = 'scheduled_datetime'
    
    fieldsets = (
        ('Información básica', {
            'fields': ('patient', 'dentist', 'scheduled_datetime', 'end_datetime')
        }),
        ('Detalles de la cita', {
            'fields': ('reason', 'status_appointment', 'notes')
        }),
    )
    
    # Método para mostrar la duración en minutos en la lista
    def get_duration_minutes(self, obj):
        return obj.duration_minutes
    get_duration_minutes.short_description = "Duración (minutos)"

        # Guardar creado por y actualizado por
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)