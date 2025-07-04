from django.db import models
from base.models import AuditoriaModel
# Create your models here.
class PacienteModel(AuditoriaModel):
    # Informacion básica del paciente
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre del Paciente')
    apellido_paterno = models.CharField(max_length=100, blank=False, null=False, verbose_name='Apellido Paterno del Paciente')
    apellido_materno = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellido Materno del Paciente')
    edad = models.PositiveIntegerField(verbose_name='Edad', help_text='Edad en años', blank=True, null=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento', help_text='Formato: YYYY-MM-DD', blank=True, null=True)
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O','Otro')], default='O', verbose_name='Género')
    # Contacto del paciente
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono de Contacto')
    email = models.EmailField(blank=True, null=True, verbose_name='Correo Electrónico')
    # Direccion del paciente
    calle = models.CharField(max_length=100, blank=True, null=True, verbose_name='Calle')
    numero = models.CharField(max_length=100, blank=True, null=True, verbose_name='Número Exterior')
    colonia = models.CharField(max_length=100, blank=True, null=True, verbose_name='Colonia')
    cp = models.CharField(max_length=10, blank=True, null=True, verbose_name='Código Postal')
    ciudad = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ciudad')
    estado = models.CharField(max_length=100, blank=True, null=True, verbose_name='Estado')
    # Información adicional del paciente
    alergias = models.TextField(blank=True, null=True, verbose_name='Alergias')
    enfermedades = models.TextField(blank=True, null=True, verbose_name='Enfermedades Preexistentes')
    antecedentes_familiares = models.TextField(blank=True, null=True, verbose_name='Antecedentes Familiares')

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno or ''}"
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['apellido_paterno', 'apellido_materno', 'nombre']
        unique_together = ('nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento')