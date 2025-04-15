from django.db import models
from paciente.models import PacienteModel
from django.contrib.auth.models import User
from tratamientos.models import TreatmentPerformed
from citas.models import Appointment
from django_prose_editor.fields import ProseEditorField
from base.models import BaseModel


class Tooth(BaseModel):
    """Catálogo de dientes según notación estándar"""
    TOOTH_TYPES = [
        ('incisor', 'Incisivo'),
        ('canine', 'Canino'),
        ('premolar', 'Premolar'),
        ('molar', 'Molar'),
    ]
    
    POSITIONS = [
        ('upper_right', 'Superior Derecha'),
        ('upper_left', 'Superior Izquierda'),
        ('lower_right', 'Inferior Derecha'),
        ('lower_left', 'Inferior Izquierda'),
    ]
    
    number = models.PositiveSmallIntegerField("Número", unique=True,
                                            help_text="Según sistema de notación universal/FDI")
    name = models.CharField("Nombre", max_length=50)
    tooth_type = models.CharField("Tipo", max_length=10, choices=TOOTH_TYPES)
    position = models.CharField("Posición", max_length=15, choices=POSITIONS)
    description = ProseEditorField("Descripción", blank=True)
    
    class Meta:
        verbose_name = "Diente"
        verbose_name_plural = "Dientes"
        unique_together = ('number', 'position')
        db_table = 'dental_tooth'
        
    def __str__(self):
        return f"#{self.number} - {self.name}"


class ToothSurface(BaseModel):
    """Superficies de dientes"""
    SURFACE_CHOICES = [
        ('V', 'Vestibular'),
        ('L', 'Lingual/Palatino'),
        ('M', 'Mesial'),
        ('D', 'Distal'),
        ('O', 'Oclusal'),
        ('I', 'Incisal'),
    ]
    
    tooth = models.ForeignKey(Tooth, on_delete=models.CASCADE, 
                            related_name='surfaces', verbose_name="Diente")
    surface = models.CharField("Superficie", max_length=1, choices=SURFACE_CHOICES)
    description = ProseEditorField("Descripción", blank=True)
    
    class Meta:
        verbose_name = "Superficie Dental"
        verbose_name_plural = "Superficies Dentales"
        unique_together = ('tooth', 'surface')
        db_table = 'dental_surface'
    
    def __str__(self):
        return f"{self.tooth} - {self.get_surface_display()}"


class Odontogram(BaseModel):
    """Registro principal del odontograma"""
    STATES = [
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
    ]
    
    patient = models.ForeignKey(PacienteModel, on_delete=models.CASCADE, 
                               related_name='odontograms', verbose_name="Paciente")
    dentist = models.ForeignKey(User, on_delete=models.PROTECT, 
                               limit_choices_to={'is_staff': True}, 
                               related_name='odontograms', verbose_name="Dentista")
    general_observations = ProseEditorField("Observaciones Generales", blank=True)
    
    class Meta:
        verbose_name = "Odontograma"
        verbose_name_plural = "Odontogramas"
    
    def __str__(self):
        return f"Odontograma de {self.patient} - {self.created_date}"
    
    def save(self, *args, **kwargs):
        """Asegurar que solo haya un odontograma activo por paciente"""
        if self.status == 'active':
            Odontogram.objects.filter(patient=self.patient, status='active').exclude(id=self.id).update(status='inactive')
        super().save(*args, **kwargs)


class ToothStatus(BaseModel):
    """Estado de cada diente en un odontograma"""
    TOOTH_STATES = [
        ('present', 'Presente'),
        ('absent', 'Ausente'),
        ('implant', 'Implante'),
        ('temporary', 'Temporal'),
        ('to_extract', 'Para Extraer'),
    ]
    
    odontogram = models.ForeignKey(Odontogram, on_delete=models.CASCADE, 
                                  related_name='tooth_status', verbose_name="Odontograma")
    tooth = models.ForeignKey(Tooth, on_delete=models.PROTECT, 
                            related_name='status_records', verbose_name="Diente")
    tooth_state = models.CharField("Estado del diente", max_length=15, 
                                 choices=TOOTH_STATES, default='present')
    recorded_date = models.DateField("Fecha de Registro", auto_now_add=True)
    dentist = models.ForeignKey(User, on_delete=models.PROTECT, 
                              limit_choices_to={'is_staff': True}, 
                              related_name='tooth_status_records', verbose_name="Dentista")
    notes = ProseEditorField("Notas", blank=True)
    
    class Meta:
        verbose_name = "Estado de Diente"
        verbose_name_plural = "Estados de Dientes"
        unique_together = ('odontogram', 'tooth')
        db_table = 'dental_tooth_status'
    
    def __str__(self):
        return f"{self.tooth} - {self.get_tooth_state_display()} ({self.odontogram.patient})"


class DentalCondition(BaseModel):
    """Condiciones dentales diagnósticadas"""
    CONDITION_TYPES = [
        ('caries', 'Caries'),
        ('restoration', 'Restauración'),
        ('crown', 'Corona'),
        ('root_canal', 'Tratamiento de Conducto'),
        ('bridge', 'Puente'),
        ('veneer', 'Carilla'),
        ('mobility', 'Movilidad'),
        ('fracture', 'Fractura'),
        ('impacted', 'Impactado'),
        ('other', 'Otro'),
    ]
    
    CONDITION_STATES = [
        ('active', 'Activa'),
        ('treated', 'Tratada'),
        ('in_treatment', 'En Tratamiento'),
        ('under_observation', 'En Observación'),
    ]
    
    tooth_status = models.ForeignKey(ToothStatus, on_delete=models.CASCADE, 
                                    related_name='conditions', verbose_name="Estado del Diente")
    surface = models.ForeignKey(ToothSurface, on_delete=models.SET_NULL, 
                              null=True, blank=True, 
                              related_name='conditions', verbose_name="Superficie")
    condition_type = models.CharField("Tipo de Condición", max_length=15, choices=CONDITION_TYPES)
    description = models.TextField("Descripción")
    diagnosis_date = models.DateField("Fecha de Diagnóstico", auto_now_add=True)
    condition_state = models.CharField("Estado de la condición", max_length=20, 
                                     choices=CONDITION_STATES, default='active')
    dentist = models.ForeignKey(User, on_delete=models.PROTECT, 
                              limit_choices_to={'is_staff': True}, 
                              related_name='diagnosed_conditions', verbose_name="Dentista")
    
    class Meta:
        verbose_name = "Condición Dental"
        verbose_name_plural = "Condiciones Dentales"
        db_table = 'dental_condition'
    
    def __str__(self):
        return f"{self.tooth_status.tooth} - {self.get_condition_type_display()}"


class ToothTreatment(BaseModel):
    """Tratamientos específicos realizados en un diente"""
    treatment_performed = models.ForeignKey(TreatmentPerformed, on_delete=models.CASCADE, 
                                          related_name='tooth_treatments', 
                                          verbose_name="Tratamiento Realizado")
    tooth = models.ForeignKey(Tooth, on_delete=models.PROTECT, 
                            related_name='treatments', verbose_name="Diente")
    surface = models.ForeignKey(ToothSurface, on_delete=models.SET_NULL, 
                              null=True, blank=True, 
                              related_name='treatments', verbose_name="Superficie")
    dental_condition = models.ForeignKey(DentalCondition, on_delete=models.SET_NULL, 
                                       null=True, blank=True, 
                                       related_name='treatments', verbose_name="Condición Tratada")
    specific_description = models.TextField("Descripción Específica")
    performed_date = models.DateField("Fecha de Realización")
    dentist = models.ForeignKey(User, on_delete=models.PROTECT, 
                              related_name='tooth_treatments', verbose_name="Dentista")
    treatment_state = models.CharField("Estado del tratamiento", max_length=15, 
                                     choices=TreatmentPerformed.STATUS_CHOICES, default='completed')
    specific_materials = models.TextField("Materiales Específicos Utilizados", blank=True)
    
    class Meta:
        verbose_name = "Tratamiento por Diente"
        verbose_name_plural = "Tratamientos por Diente"
        db_table = 'dental_tooth_treatment'
    
    def __str__(self):
        return f"{self.tooth} - {self.treatment_performed.treatment}"
    
    def save(self, *args, **kwargs):
        """Actualizar automáticamente el estado de la condición dental asociada"""
        super().save(*args, **kwargs)
        if self.dental_condition and self.treatment_state == 'completed':
            self.dental_condition.condition_state = 'treated'
            self.dental_condition.save()


class DentalDocument(BaseModel):
    """Documentos clínicos dentales (radiografías, fotografías, etc.)"""
    DOCUMENT_TYPES = [
        ('xray', 'Radiografía'),
        ('panoramic', 'Panorámica'),
        ('photo', 'Fotografía'),
        ('consent', 'Consentimiento'),
        ('report', 'Informe'),
        ('other', 'Otro'),
    ]
    
    patient = models.ForeignKey(PacienteModel, on_delete=models.CASCADE, 
                              related_name='dental_documents', verbose_name="Paciente")
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, 
                                  null=True, blank=True,
                                  related_name='documents', verbose_name="Cita")
    document_type = models.CharField("Tipo de Documento", max_length=10, choices=DOCUMENT_TYPES)
    file = models.FileField("Archivo", upload_to='dental_documents/%Y/%m/')
    uploaded_date = models.DateField("Fecha de Subida", auto_now_add=True)
    title = models.CharField("Título", max_length=200)
    description = ProseEditorField("Descripción", blank=True)
    teeth = models.ManyToManyField(Tooth, blank=True, 
                                 related_name='documents', verbose_name="Dientes Relacionados")
    
    class Meta:
        verbose_name = "Documento Dental"
        verbose_name_plural = "Documentos Dentales"
        db_table = 'dental_document'
    
    def __str__(self):
        return f"{self.title} - {self.patient}"