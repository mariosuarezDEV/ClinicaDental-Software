from django.db import models
from base.models import AuditoriaModel
from paciente.models import PacienteModel # Necesario para poner la cita de un paciente
# Create your models here.

class CitaModel(AuditoriaModel):
    paciente = models.ForeignKey(PacienteModel, on_delete=models.PROTECT, related_name='citas', verbose_name='Paciente')
    fecha_cita = models.DateTimeField(verbose_name='Fecha y Hora de la Cita')
    motivo = models.TextField(blank=True, null=True, verbose_name='Motivo de la Cita')
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada')
    ], default='pendiente', verbose_name='Estado de la Cita')

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['fecha_cita']
        unique_together = ('paciente', 'fecha_cita')
    def __str__(self):
        return f"Cita de {self.paciente} - {self.fecha_cita.strftime('%Y-%m-%d')} ({self.estado})"