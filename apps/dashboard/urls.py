from django.urls import path
from . import views

urlpatterns = [
    # Dashboard principal
    path('', views.mainDashboard, name='main_dashboard'),
    
    # Gestión de KPIs
    path('kpi/', views.mainDashboard, name='view_kpis'),
    path('kpi/create/', views.create_KPI, name='create_kpi'),
    path('kpi/<int:kpi_id>/update/', views.update_KPI, name='update_kpi'),
    path('kpi/<int:kpi_id>/delete/', views.delete_KPI, name='delete_kpi'),
    path('kpi/<int:kpi_id>/', views.view_KPI_details, name='view_kpi_details'),
    
    # Gestión de metas de KPIs
    path('kpi/goals/', views.view_KPI_goal, name='view_kpi_goals'),
    path('kpi/goals/<int:kpi_goal_id>/edit/', views.edit_KPI_goal, name='edit_kpi_goal'),
    path('kpi/goals/<int:kpi_goal_id>/delete/', views.delete_KPI_goal, name='delete_kpi_goal'),
    path('kpi/goals/create/', views.create_KPI_target, name='create_kpi_target'),

    # Rutas para calculo de KPI
    path('kpi/<str:kpi_name>/', views.calcular_kpi, name='calcular_kpi'),

]