from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Rutas para gestión de usuarios (empleados)
    path('create_user/', views.create_user, name='create_user'),
    path('delete_user/<int:empleado_id>/', views.delete_user, name='delete_user'),
    path('update_user/<int:empleado_id>/', views.update_user, name='update_user'),
    path('view_users/', views.view_users, name='view_users'),
    path('view_user/<int:empleado_id>/', views.view_user, name='view_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Ruta para autenticación
    path('login/', views.login_view, name='login'),
]