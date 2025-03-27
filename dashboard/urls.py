from django.urls import path
from . import views

urlpatterns = [
    path("main_dashboard/", views.mainDashboard, name="main_dashboard"),
    path("create_kpi/", views.create_kpi, name="create_kpi"),
    path("update_kpi/<int:kpi_id>/", views.update_KPI, name="update_kpi"),
    path("delete_kpi/<int:kpi_id>", views.delete_KPI, name="delete_kpi"),
    path("kpi_details/<int:kpi_id>/", views.view_KPI_details, name="kpi_details")
]