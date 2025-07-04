from django.db import models
from base.models import AuditoriaModel
from paciente.models import PacienteModel
from doctor.models import DoctorModel
# Create your models here.

class CategoriaTratamientoModel(AuditoriaModel):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre de la Categoría')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción de la Categoría')

    class Meta:
        verbose_name = 'Categoría de Tratamiento'
        verbose_name_plural = 'Categorías de Tratamiento'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class TratamientoModel(AuditoriaModel):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre del Tratamiento')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción del Tratamiento')
    categoria = models.ForeignKey(CategoriaTratamientoModel, on_delete=models.PROTECT, related_name='tratamientos', verbose_name='Categoría de Tratamiento')
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo del Tratamiento')

    class Meta:
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'
        ordering = ['nombre']

    def __str__(self):
        return f'Tratamiento {self.nombre}. Costo: {self.costo} - {self.categoria.nombre}'

class TratamientoPacienteModel(AuditoriaModel):
    paciente = models.ForeignKey(PacienteModel, on_delete=models.PROTECT, related_name='tratamientos', verbose_name='Paciente')
    tratamiento = models.ForeignKey(TratamientoModel, on_delete=models.PROTECT, related_name='pacientes', verbose_name='Tratamiento')
    doctor = models.ForeignKey(DoctorModel, on_delete=models.PROTECT, related_name='tratamientos', verbose_name='Doctor Asignado')
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio del Tratamiento')
    fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de Fin del Tratamiento')
    estado = models.CharField(max_length=20, choices=[
        ('activo', 'Activo'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado')
    ], default='activo', verbose_name='Estado del Tratamiento')

    class Meta:
        verbose_name = 'Tratamiento del Paciente'
        verbose_name_plural = 'Tratamientos de los Pacientes'
        ordering = ['fecha_inicio']

    def __str__(self):
        return f'Tratamiento {self.tratamiento.nombre} para {self.paciente} - Estado: {self.estado}'