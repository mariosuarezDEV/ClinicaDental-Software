from django.urls import path
from .views import FormCalculatorView, FinancingResultView

urlpatterns = [
    path("calculator/", FormCalculatorView.as_view(), name="form_calculator"),
    path("result/", FinancingResultView.as_view(), name="financing_result"),
]
