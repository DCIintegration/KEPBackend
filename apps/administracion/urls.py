from django.urls import path
from . import views

urlpatterns = [
    path('inputFinantialData/', views.inputFinantialData, name='input-finantial-data'),
    path('viewFinantialHistory/', views.viewFinantialHistory, name='view-finantial-history'),
    path('ingresoActividad/', views.IngresoActividadListCreateView.as_view(), name='ingreso-actividad-list-create'),
    path('ingresoActividad/<int:pk>/', views.IngresoActividadRetrieveUpdateDestroyView.as_view(), name='ingreso-actividad-detail'),
]