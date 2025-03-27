from django.urls import path
from . import views

urlpatterns = [
    path("dashboard_administrativo/", views.dashboard_administrativo, name="dashboard_administrativo"),
    path("departamento_detalles/", views.departamento_detalles, name="departamento_detalles"),
    path("empleado_detalles/<int:empleado_id>/", views.empleado_detalles, name= "empleado_detalles"),
    path("modificar_datos/<int:empleado_id>", views.modificar_datos, name= "modificar_datos")
]