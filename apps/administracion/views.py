from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import FinantialData, IngresoActividad
from apps.administracion.serializers import  IngresoActividadSerializer
from .serializers import FinantialDataSerializer
from rest_framework import status, generics

"""-------- ENDPOINTS PARA INFORMACIÓN FINANCIERA ----------"""

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def inputFinantialData(request):
    """
    Endpoint para alimentar el sistema con nuevos datos financieros.
    Solo se podrá alimentar información del mes actual. Para otros casos,
    se requerirá autorización de gerencia y administración.
    """
    serializer = FinantialDataSerializer(data=request.data)
    if serializer.is_valid():
        finantial_data = serializer.save()
        return Response(
            {
                "message": f"Datos financieros para ({finantial_data.month}/{finantial_data.year}) creados exitosamente"
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"message": "Consulte al departamento de sistemas", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def viewFinantialHistory(request):
    """
    Retorna todo el historial financiero.
    """
    data = FinantialData.objects.all().order_by('-year', '-month')
    serializer = FinantialDataSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class IngresoActividadListCreateView(generics.ListCreateAPIView):
    queryset = IngresoActividad.objects.all()
    serializer_class = IngresoActividadSerializer
    permission_classes = [IsAuthenticated]


class IngresoActividadRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IngresoActividad.objects.all()
    serializer_class = IngresoActividadSerializer
    permission_classes = [IsAuthenticated]