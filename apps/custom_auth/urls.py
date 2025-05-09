from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
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
]