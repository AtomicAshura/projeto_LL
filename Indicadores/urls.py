from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import IndicadorAPI

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('logout/', LogoutView.as_view(next_page= '/'), name= 'logout'),
    path('api/indicadores/',IndicadorAPI.as_view(), name='api-indicadores')
]