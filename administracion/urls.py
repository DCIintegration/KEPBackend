from django.urls import path
from . import views

urlpatterns = [
    path("dashboard_administrativo/", views.dashboard_administrativo, name="dashboard_administrativo"),
]