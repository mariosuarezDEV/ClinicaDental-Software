from django.urls import path
from .views import (
    ListTreatmentsView,
    CreateTreatmentView,
    UpdateTreatmentView,
    DeleteTreatmentView,
)

urlpatterns = [
    path("", ListTreatmentsView.as_view(), name="lista_tratamientos"),
    path("crear/", CreateTreatmentView.as_view(), name="crear_tratamiento"),
    path("editar/<int:pk>/", UpdateTreatmentView.as_view(), name="editar_tratamiento"),
    path(
        "eliminar/<int:pk>/", DeleteTreatmentView.as_view(), name="eliminar_tratamiento"
    ),
]
