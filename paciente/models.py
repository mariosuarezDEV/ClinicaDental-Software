from django.db import models
from base.models import BaseModel
from django_prose_editor.fields import ProseEditorField
# Create your models here.
class PacienteModel(BaseModel):
    nombre = models.CharField(max_length=100, null=False, blank=False, verbose_name="Nombre", help_text="Nombre del paciente", error_messages={"required": "Este campo es obligatorio"})
    apellido = models.CharField(max_length=100, null=False, blank=False, verbose_name="Apellido", help_text="Apellido del paciente", error_messages={"required": "Este campo es obligatorio"})
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    nombre_completo.fget.short_description = "Nombre completo"
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimiento", help_text="Fecha de nacimiento del paciente")
    # Direccion
    calle = models.CharField(max_length=100, null=True, blank=True, verbose_name="Calle", help_text="Calle del paciente")
    numero = models.CharField(max_length=10, null=True, blank=True, verbose_name="Número", help_text="Número de la calle del paciente")
    colonia = models.CharField(max_length=100, null=True, blank=True, verbose_name="Colonia", help_text="Colonia del paciente")
    cp = models.CharField(max_length=10, null=True, blank=True, verbose_name="Código postal", help_text="Código postal del paciente")
    ciudad = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ciudad", help_text="Ciudad del paciente")
    estado = models.CharField(max_length=100, null=True, blank=True, verbose_name="Estado", help_text="Estado del paciente")
    pais = models.CharField(max_length=100, null=True, blank=True, verbose_name="País", help_text="País del paciente")
    @property
    def direccion_completa(self):
        return f"{self.calle} {self.numero}, {self.colonia}, {self.cp}, {self.ciudad}, {self.estado}, {self.pais}"
    direccion_completa.fget.short_description = "Dirección completa"
    # Control de credito
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Límite de crédito", help_text="Límite de crédito del paciente")
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Saldo actual", help_text="Saldo actual del paciente")
    # Contacto
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono", help_text="Teléfono del paciente")
    celular = models.CharField(max_length=15, null=True, blank=True, verbose_name="Celular", help_text="Celular del paciente")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="Email", help_text="Email del paciente")
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        db_table = "pacientes"
    
    def __str__(self):
        return f"{self.nombre_completo}"

class HistorialMedicoPaciente(BaseModel):
    """Historial médico del paciente"""
    paciente = models.OneToOneField(PacienteModel, on_delete=models.CASCADE, related_name='historial_medico', verbose_name="Paciente")
    allergies = ProseEditorField("Alergias", blank=True, help_text="Alergias del paciente")
    medical_conditions = ProseEditorField("Condiciones Médicas", blank=True, help_text="Condiciones médicas del paciente")
    current_medications = ProseEditorField("Medicamentos Actuales", blank=True, help_text="Medicamentos actuales del paciente")
    past_medications = ProseEditorField("Medicamentos Pasados", blank=True, help_text="Medicamentos pasados del paciente")
    blood_type = models.CharField("Tipo de Sangre", max_length=5, blank=True, help_text="Tipo de sangre del paciente")
    last_update = models.DateField("Última Actualización", auto_now=True, help_text="Última actualización del historial médico")
    additional_notes = ProseEditorField("Notas Adicionales", blank=True, help_text="Notas adicionales sobre el paciente")
    
    class Meta:
        verbose_name = "Historial Médico"
        verbose_name_plural = "Historiales Médicos"
        db_table = "historiales_medicos"
    
    def __str__(self):
        return f"Historial de {self.paciente.nombre_completo}"