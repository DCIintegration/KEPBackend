from django.urls import path
from . import views

urlpatterns = [
    # Rutas de usuarios
    path('register/', views.UserRegistrationView.as_view(), name='register_user'),
    path('profile/', views.getUserProfile, name='user_profile'),
    path('delete/<int:custom_user_id>/', views.deleteUser, name='delete_user'),
    path('update/<int:custom_user_id>/', views.updateUser, name='update_user'),
    path('get/<int:custom_user_id>/', views.getUser, name='get_user'),
    path('list/', views.listUsers, name='list_users'),
    path('logout/', views.logoutUser, name='logout_user'),
    # Rutas de empleados
    path('empleados/', views.listEmployees, name='list_empleados'),
    path('empleados/<int:empleado_id>/', views.employeeDetails, name='detalle_empleado'),
    path('empleados/create/', views.createEmployee, name='crear_empleado'),
    path('empleados/update/<int:empleado_id>/', views.updateEmployee, name='actualizar_empleado'),
    path('empleados/delete/<int:empleado_id>/', views.deleteEmployee, name='eliminar_empleado'),
    # Rutas de departamentos
    path('departamentos/', views.listDepartment, name='list_departamentos'),
    path('departamentos/<int:departamento_id>/', views.departmentDetails, name='detalle_departamento'),
    # Rutas para informacion de KPIs
    path('finanzas/nomina/<int:departamento_id>/', views.nominaDepartamento, name='nomina_departamento'),
    path('finanzas/info/', views.infoFinancieraGlobal, name='info_financiera_global'),

]