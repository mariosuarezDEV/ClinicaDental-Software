from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class AuditoriaModel(models.Model):
    # Informacion basica de la auditoria
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_auditoria_creacion')
    usuario_actualizacion = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_auditoria_actualizacion')

    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones Adicionales')
    soft_delete = models.BooleanField(default=False, verbose_name='Eliminado Lógicamente')
    class Meta:
        abstract = True
    def __str__(self):
        return f"Auditoria {self.id} - Creado por {self.usuario_creacion.username} el {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"