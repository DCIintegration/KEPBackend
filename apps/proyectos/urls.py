from django.urls import path
from . import views

urlpatterns = [
    # Gestión de logs KPI
    path('logs/', views.view_logs, name='view_logs'),
    path('logs/<int:KpiInputData_id>/', views.view_log_details, name='view_log_details'),
    path('logs/<int:KpiInputData_id>/report/', views.report_log, name='report_log'),
    path('logs/<int:KpiInputData_id>/modify/', views.modify_log, name='modify_log'),
    path('logs/upload/manual/', views.upload_manual_log, name='upload_manual_log'),
    path('proyectos/', views.ProyectoListCreateView.as_view(), name='proyecto-list-create'),
    path('proyectos/<int:pk>/', views.ProyectoRetrieveUpdateDestroyView.as_view(), name='proyecto-detail'),
    path('asignaciones/', views.AsignacionProyectoListCreateView.as_view(), name='asignacion-list-create'),
    path('asignaciones/<int:pk>/', views.AsignacionProyectoRetrieveUpdateDestroyView.as_view(), name='asignacion-detail'),
    path("registro_horas/upload/", views.upload_csv, name="upload_registro_horas"),
]