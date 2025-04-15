from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from django_prose_editor.fields import ProseEditorField
from citas.models import Appointment

class TreatmentCategory(BaseModel):
    """Categorías de tratamientos dentales"""
    name = models.CharField("Nombre", max_length=100)
    description = models.TextField("Descripción", blank=True)
    color_code = models.CharField("Código de Color", max_length=7, blank=True, help_text="Código HEX para representación visual")
    
    class Meta:
        verbose_name = "Categoría de Tratamiento"
        verbose_name_plural = "Categorías de Tratamientos"
        db_table = 'tratamiento_categoria'
    
    def __str__(self):
        return self.name


class Treatment(BaseModel):
    """Catálogo de tratamientos disponibles"""
    name = models.CharField("Nombre", max_length=200)
    description = ProseEditorField("Descripción" , blank=True, null=True)
    category = models.ForeignKey(TreatmentCategory, on_delete=models.PROTECT, 
                                related_name='treatments', verbose_name="Categoría")
    base_price = models.DecimalField("Precio Base", max_digits=10, decimal_places=2)
    estimated_duration = models.PositiveIntegerField("Duración Estimada (minutos)")
    requires_laboratory = models.BooleanField("Requiere Laboratorio", default=False)
    laboratory_price = models.DecimalField("Precio de Laboratorio", max_digits=10, decimal_places=2, blank=True, null=True)
    notes = ProseEditorField("Notas", blank=True)
    
    class Meta:
        verbose_name = "Tratamiento"
        verbose_name_plural = "Tratamientos"
        ordering = ['category', 'name']
        db_table = 'tratamientos'
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class TreatmentPerformed(BaseModel):
    """Registro de tratamientos realizados"""
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE,
                                  related_name='treatments_performed', verbose_name="Cita")
    treatment = models.ForeignKey(Treatment, on_delete=models.PROTECT, 
                                related_name='performances', verbose_name="Tratamiento")
    dentist = models.ForeignKey(User, on_delete=models.PROTECT, 
                               related_name='treatments_performed', verbose_name="Dentista")
    applied_price = models.DecimalField("Precio Aplicado", max_digits=10, decimal_places=2, 
                                      help_text="Precio final aplicado (puede incluir descuentos)")
    start_datetime = models.DateTimeField("Fecha y Hora de Inicio", null=True, blank=True)
    end_datetime = models.DateTimeField("Fecha y Hora de Finalización", null=True, blank=True)
    status = models.CharField("Estado", max_length=15, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField("Observaciones", blank=True)
    
    dentist = models.ForeignKey(User, on_delete=models.PROTECT, 
                               related_name='treatments_performed', verbose_name="Dentista")
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE,
                                  related_name='treatments_performed', verbose_name="Cita")
    class Meta:
        verbose_name = "Tratamiento Realizado"
        verbose_name_plural = "Tratamientos Realizados"
        db_table = 'performed_treatments'
        ordering = ['-start_datetime']
    
    def __str__(self):
        return f"{self.treatment} - {self.appointment}"
    
    @property
    def duration_minutes(self):
        """Calcular la duración real del tratamiento en minutos"""
        if self.start_datetime and self.end_datetime:
            duration = self.end_datetime - self.start_datetime
            return int(duration.total_seconds() / 60)
        return None