from django.urls import path
from .views import OdontogramView, CreateTeethView

urlpatterns = [
    path("", OdontogramView.as_view(), name="odontograma"),
    path("teeth/create/", CreateTeethView.as_view(), name="create_teeth"),
]
