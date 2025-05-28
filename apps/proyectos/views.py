import datetime
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.dashboard.models import KpiInputData
from .models import Proyecto, AsignacionProyecto
from .serializers import ProyectoSerializer, AsignacionProyectoSerializer
from apps.dashboard.serializers import KpiInputDataSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import pandas as pd
import io
from .tosql import LoadData

def has_proyectos_permission(user):
    """
    Función auxiliar para verificar si un usuario tiene permisos de proyectos o es superusuario.
    """
    return user.is_superuser 


class ProyectoListCreateView(generics.ListCreateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]


class ProyectoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]

# CRUD para AsignacionProyecto
class AsignacionProyectoListCreateView(generics.ListCreateAPIView):
    queryset = AsignacionProyecto.objects.all()
    serializer_class = AsignacionProyectoSerializer
    permission_classes = [IsAuthenticated]

class AsignacionProyectoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AsignacionProyecto.objects.all()
    serializer_class = AsignacionProyectoSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_logs(request):
    """
    Vista para ver todos los logs de KPI.
    Disponible para superusuarios y usuarios con permiso de proyectos.
    """
    if not has_proyectos_permission(request.user):
        return Response(
            {"error": "No tienes permiso para ver esta pagina"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    logs = KpiInputData.objects.all().order_by('-created_at')
    serializer = KpiInputDataSerializer(logs, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_log_details(request, KpiInputData_id):
    """
    Vista para ver detalles de un log específico.
    Disponible para superusuarios y usuarios con permiso de proyectos.
    """
    if not has_proyectos_permission(request.user):
        return Response(
            {"error": "No tienes permiso para ver esta pagina"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        log = KpiInputData.objects.get(id=KpiInputData_id)
        serializer = KpiInputDataSerializer(log)
        return Response(serializer.data)
    except KpiInputData.DoesNotExist:
        return Response(
            {"error": "Log no encontrado"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_log(request, KpiInputData_id):
    """
    Método para reportar un log. Generará un mail al equipo de sistemas para editar ese log.
    Disponible para superusuarios y usuarios con permiso de proyectos.
    """
    if not has_proyectos_permission(request.user):
        return Response(
            {"error": "No tienes permiso para reportar logs"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        log = KpiInputData.objects.get(id=KpiInputData_id)
        log.status = "reportado"
        log.save()
        
        # Queda pendiente lógica de notificaciones vía correo electrónico para el equipo de sistemas
        
        return Response({"message": "Log reportado correctamente"})
    except KpiInputData.DoesNotExist:
        return Response(
            {"error": "Log no encontrado"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def modify_log(request, KpiInputData_id):
    """
    Modifica un log existente.
    Solo disponible para superusuarios.
    """
    if not request.user.is_superuser:
        return Response(
            {"error": "No tienes permiso para modificar logs"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        log = KpiInputData.objects.get(id=KpiInputData_id)
        serializer = KpiInputDataSerializer(log, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Log modificado correctamente"})
        
        return Response(
            {"error": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except KpiInputData.DoesNotExist:
        return Response(
            {"error": "Log no encontrado"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_manual_log(request):
    """
    Carga manual de datos de KPI.
    Disponible para superusuarios y usuarios con permiso de proyectos.
    """
    serializer = KpiInputDataSerializer(data=request.data)
    
    if serializer.is_valid():
        # Crear el nuevo registro
        log = serializer.save()
        return Response(
            {"message": f"Log creado exitosamente", "id": log.id},
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_csv(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No se envió ningún archivo"}, status=status.HTTP_400_BAD_REQUEST)

    if not file.name.endswith('.csv'):
        return Response({"error": "El archivo debe ser un CSV"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        LoadData.load_csv(file)
        return Response({"message": "Archivo procesado correctamente"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Ocurrió un error al procesar el archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)