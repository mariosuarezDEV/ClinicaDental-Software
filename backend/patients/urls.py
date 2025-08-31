from django.urls import path
from .views import (
    CreatePatientView,
    ListPatientsView,
    DeletePatientView,
    UpdatePatientView,
)

urlpatterns = [
    path("crear/", CreatePatientView.as_view(), name="crear_paciente"),
    path("listar/", ListPatientsView.as_view(), name="listar_pacientes"),
    path("eliminar/<int:pk>/", DeletePatientView.as_view(), name="eliminar_paciente"),
    path(
        "actualizar/<int:pk>/", UpdatePatientView.as_view(), name="actualizar_paciente"
    ),
]
