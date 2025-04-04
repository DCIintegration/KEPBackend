from django.urls import path
from . import views

urlpatterns = [
    path("view_logs/", views.view_logs, name="view_logs"),
    path("view_log_details/<int:KpiInputData_id>", views.view_log_details, name="view_log_details"),
    path("report_log/", views.report_log, name="report_log"),
    path("upload_excel_log/", views.upload_excel_log, name="upload_excel_log"),
    path("upload_manual_log/", views.upload_manual_log, name="upload_manual_log"),
    path("modify_log/<int:KpiInputData_id>/", views.modify_log, name="modify_log"),
]