from django.db import models
from paciente.models import PacienteModel
from django.contrib.auth.models import User
from django_prose_editor.fields import ProseEditorField
class Appointment(models.Model):
    """Modelo para agendar citas"""
    STATUS_CHOICES = [
        ('scheduled', 'Programada'),
        ('confirmed', 'Confirmada'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
        ('no_show', 'No Asistió'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, 
                              related_name='appointments', verbose_name="Paciente")
    dentist = models.ForeignKey(StaffMember, on_delete=models.CASCADE,
                               limit_choices_to={'role': 'dentist'}, 
                               related_name='appointments', verbose_name="Dentista")
    scheduled_datetime = models.DateTimeField("Fecha y Hora Programada")
    end_datetime = models.DateTimeField("Fecha y Hora de Finalización Esperada")
    reason = models.TextField("Motivo de Consulta")
    status = models.CharField("Estado", max_length=15, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField("Notas", blank=True)
    created_at = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    created_by = models.ForeignKey(StaffMember, on_delete=models.SET_NULL, null=True,
                                  related_name='appointments_created', verbose_name="Creado Por")
    
    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-scheduled_datetime']
    
    def __str__(self):
        return f"{self.patient} - {self.scheduled_datetime.strftime('%d/%m/%Y %H:%M')}"
    
    @property
    def duration_minutes(self):
        """Duración programada en minutos"""
        duration = self.end_datetime - self.scheduled_datetime
        return int(duration.total_seconds() / 60)


class AppointmentReminder(models.Model):
    """Sistema de recordatorios para citas"""
    REMINDER_TYPE_CHOICES = [
        ('email', 'Correo Electrónico'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('phone', 'Llamada Telefónica'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('sent', 'Enviado'),
        ('failed', 'Fallido'),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE,
                                   related_name='reminders', verbose_name="Cita")
    reminder_type = models.CharField("Tipo de Recordatorio", max_length=10, choices=REMINDER_TYPE_CHOICES)
    scheduled_datetime = models.DateTimeField("Fecha y Hora Programada")
    status = models.CharField("Estado", max_length=10, choices=STATUS_CHOICES, default='pending')
    sent_datetime = models.DateTimeField("Fecha y Hora de Envío", null=True, blank=True)
    notes = models.TextField("Notas", blank=True)
    
    class Meta:
        verbose_name = "Recordatorio de Cita"
        verbose_name_plural = "Recordatorios de Citas"
    
    def __str__(self):
        return f"Recordatorio {self.get_reminder_type_display()} - {self.appointment}"