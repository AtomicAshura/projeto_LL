from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('logout/', LogoutView.as_view(next_page= '/'), name= 'logout')
]