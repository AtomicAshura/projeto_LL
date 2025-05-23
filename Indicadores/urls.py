from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from .views import IndicadorAPI, UploadPlanilhaAPI

urlpatterns = [
    # Frontend
    path("", views.dashboard, name="dashboard"),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    ]