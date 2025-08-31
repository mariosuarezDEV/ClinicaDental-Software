from django.db import models
from django.contrib.auth.models import AbstractUser

TYPE_USER = (
    ("doctor", "Doctor"),
    ("secretary", "Secretaria"),
    ("patient", "Paciente"),
    ("assistant", "Asistente"),
)


class UserModel(AbstractUser):
    type_user = models.CharField(
        max_length=20,
        choices=TYPE_USER,
        default="patient",
        null=True,
        blank=True,
        verbose_name="Tipo de Usuario",
    )
    # Information
    phone = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Teléfono"
    )
    date_birth = models.DateField(
        null=True, blank=True, verbose_name="Fecha de Nacimiento"
    )
    address = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Dirección"
    )

    def __str__(self):
        return self.get_full_name() or self.username


class AuditModel(models.Model):
    created_by = models.ForeignKey(
        UserModel, on_delete=models.PROTECT, related_name="%(class)s_created_by"
    )
    updated_by = models.ForeignKey(
        UserModel, on_delete=models.PROTECT, related_name="%(class)s_updated_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
