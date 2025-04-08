from django.urls import path
from .views import PacienteListView, PacienteDetailView, PacienteWizardView

urlpatterns = [
    path('', PacienteListView.as_view(), name='paciente_list'),
    path('nuevo/', PacienteWizardView.as_view(), name='paciente_create'),
    path('<int:pk>/', PacienteDetailView.as_view(), name='paciente_detail'),
]
