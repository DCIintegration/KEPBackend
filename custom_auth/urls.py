from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("create_user/" , views.create_user, name="create_user"),
    path("delete_user/<int:empleado_id>", views.delete_user, name= "delete_user"),
    path("update_user/<int:empleado_id>", views.update_user, name= "update_user"),
    path("view_users/", views.view_users, name= "view_users"),
]