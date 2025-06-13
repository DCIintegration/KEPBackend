from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import  IngresoActividad
from apps.administracion.serializers import  IngresoActividadSerializer

from rest_framework import status, generics

"""-------- ENDPOINTS PARA INFORMACIÓN FINANCIERA ----------"""

class IngresoActividadListCreateView(generics.ListCreateAPIView):
    queryset = IngresoActividad.objects.all()
    serializer_class = IngresoActividadSerializer
    permission_classes = [IsAuthenticated]


class IngresoActividadRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IngresoActividad.objects.all()
    serializer_class = IngresoActividadSerializer
    permission_classes = [IsAuthenticated]