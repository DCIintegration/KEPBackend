from django.urls import path
from . import views

urlpatterns = [
    #Rutas para alimentar infromacion adminstrativa
    path('inputFinantialData/', views.inputFinantialData, name='input-finantial-data'),
    path('viewFinantialHistory/', views.viewFinantialHistory, name='view-finantial-history'),
]