from django.urls import path
from .views import (
    ListTreatmentsView,
    CreateTreatmentView,
    UpdateTreatmentView,
    DeleteTreatmentView,
    ListSpecialtiesView,
    CreateSpecialtyView,
    UpdateSpecialtyView,
    DeleteSpecialtyView,
)

urlpatterns = [
    path("", ListTreatmentsView.as_view(), name="lista_tratamientos"),
    path("crear/", CreateTreatmentView.as_view(), name="crear_tratamiento"),
    path("editar/<int:pk>/", UpdateTreatmentView.as_view(), name="editar_tratamiento"),
    path(
        "eliminar/<int:pk>/", DeleteTreatmentView.as_view(), name="eliminar_tratamiento"
    ),
    path("especialidades/", ListSpecialtiesView.as_view(), name="lista_especialidades"),
    path(
        "especialidades/crear/",
        CreateSpecialtyView.as_view(),
        name="crear_especialidad",
    ),
    path(
        "especialidades/editar/<int:pk>/",
        UpdateSpecialtyView.as_view(),
        name="editar_especialidad",
    ),
    path(
        "especialidades/eliminar/<int:pk>/",
        DeleteSpecialtyView.as_view(),
        name="eliminar_especialidad",
    ),
]
