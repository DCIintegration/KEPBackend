import datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.dashboard.models import KpiInputData
from .serializers import CompanyKPISerializer, KpiInputDataSerializer

def has_proyectos_permission(user):
    """
    Función auxiliar para verificar si un usuario tiene permisos de proyectos o es superusuario.
    """
    return user.is_superuser or user.is_proyectos()

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
        serializer = CompanyKPISerializer(log)
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
def upload_excel_log(request):
    """
    Carga un archivo Excel para generar logs de KPI.
    Disponible para superusuarios y usuarios con permiso de proyectos.
    """
    if not has_proyectos_permission(request.user):
        return Response(
            {"error": "No tienes permiso para ver esta página"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            file = request.FILES['file']
            period_str = request.data.get('period')
            file_type = request.data.get('file_type', 'total')
            
            # Validar y convertir la fecha
            try:
                if period_str:
                    period = datetime.datetime.strptime(period_str, '%Y-%m-%d').date()
                else:
                    # Si no se proporciona una fecha, usar el primer día del mes actual
                    today = datetime.datetime.now()
                    period = datetime.datetime(today.year, today.month, 1).date()
            except ValueError:
                return Response(
                    {"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verificar si ya existe un registro para este período y tipo de archivo
            existing = KpiInputData.objects.filter(period=period, file_type=file_type).first()
            
            if existing:
                # Actualizar registro existente
                existing.raw_data_file.delete(save=False)  # Eliminar archivo antiguo
                existing.raw_data_file = file
                existing.save()
                kpi_data = existing
            else:
                # Crear nuevo registro
                kpi_data = KpiInputData(
                    period=period,
                    file_type=file_type,
                    raw_data_file=file
                )
                kpi_data.save()
            
            # Calcular KPIs si se tienen todos los datos necesarios
            kpi_results = kpi_data.calcular_kpis()
            
            response_data = {
                "message": "Archivo subido y procesado correctamente",
                "id": kpi_data.id,
                "period": period.strftime('%Y-%m-%d'),
                "file_type": kpi_data.get_file_type_display(),
                "total_horas_facturables": kpi_data.total_horas_facturables,
                "total_horas_planta": kpi_data.total_horas_planta,
                "numero_empleados": kpi_data.numero_empleados
            }
            
            if kpi_results:
                response_data["kpis"] = kpi_results
            
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {"error": f"Error al procesar el archivo: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # Si es GET o no hay archivo, devolver mensaje
    return Response(
        {"error": "No se ha subido ningún archivo"}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_manual_log(request):
    """
    Carga manual de datos de KPI.
    Disponible para superusuarios y usuarios con permiso de proyectos.
    """
    if not has_proyectos_permission(request.user):
        return Response(
            {"error": "No tienes permiso para ver esta pagina"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = KpiInputDataSerializer(data=request.data)
    
    if serializer.is_valid():
        # Verificar si ya existe un registro similar
        if KpiInputData.objects.filter(
            period=serializer.validated_data.get('period', datetime.date.today()),
            file_type=serializer.validated_data.get('file_type', 'manual')
        ).exists():
            return Response(
                {"error": "Este log ya existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
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