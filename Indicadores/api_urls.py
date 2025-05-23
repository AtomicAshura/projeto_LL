from django.urls import path
from .views import IndicadorAPI, UploadPlanilhaAPI

urlpatterns = [
    path('indicadores/', IndicadorAPI.as_view(), name='api-indicadores'),
    path('upload-planilha/', UploadPlanilhaAPI.as_view(), name='upload-planilha'),
]