from django.db import models
from base.models import AuditoriaModel
# Create your models here.

class DoctorModel(AuditoriaModel):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre del Doctor')
    especialidad = models.CharField(max_length=100, verbose_name='Especialidad del Doctor')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono del Doctor')
    email = models.EmailField(blank=True, null=True, verbose_name='Email del Doctor')

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'
        ordering = ['nombre']

    def __str__(self):
        return f'Doctor {self.nombre} - Especialidad: {self.especialidad}'