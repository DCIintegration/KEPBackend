from django.urls import path
from . import views

urlpatterns = [
    # Gestión de logs KPI
    path('logs/', views.view_logs, name='view_logs'),
    path('logs/<int:KpiInputData_id>/', views.view_log_details, name='view_log_details'),
    path('logs/<int:KpiInputData_id>/report/', views.report_log, name='report_log'),
    path('logs/<int:KpiInputData_id>/modify/', views.modify_log, name='modify_log'),
    path('logs/upload/excel/', views.upload_excel_log, name='upload_excel_log'),
    path('logs/upload/manual/', views.upload_manual_log, name='upload_manual_log'),
]