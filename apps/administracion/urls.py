from django.urls import path
from . import views

urlpatterns = [
    # Dashboard administrativo
    path('dashboard/', views.dashboard_administrativo, name='dashboard_administrativo'),
    
    # Detalles de departamento
    path('departamentos/<int:departamento_id>/', views.departamento_detalles, name='departamento_detalles'),
    
    # Detalles y modificación de empleados
    path('empleados/<int:empleado_id>/', views.empleado_detalles, name='empleado_detalles'),
    path('empleados/<int:empleado_id>/modificar/', views.modificar_datos, name='modificar_datos'),
]