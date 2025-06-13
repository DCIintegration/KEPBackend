from django.urls import path
from . import views

urlpatterns = [
    path('ingresoActividad/', views.IngresoActividadListCreateView.as_view(), name='ingreso-actividad-list-create'),
    path('ingresoActividad/<int:pk>/', views.IngresoActividadRetrieveUpdateDestroyView.as_view(), name='ingreso-actividad-detail'),
]