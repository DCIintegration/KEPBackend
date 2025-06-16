from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.dashboard.models import Kpi, KpiTarget
from .serializers import KpiSerializer, KpiTargetSerializer
from .utils import KPI_Calculator, KPIDataCollector
import datetime



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mainDashboard(request):
    """
    Vista disponible para todos los usuarios, muestra los KPIs.
    """
    kpis = Kpi.objects.all()
    serializer = KpiSerializer(kpis, many=True)
    return Response({"KPIs": serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_KPI(request):
    """
    Vista disponible solo para el superusuario.
    Crea un nuevo KPI.
    """
    
    serializer = KpiSerializer(data=request.data)
    if serializer.is_valid():
        # Verificar si ya existe un KPI con el mismo código
        if Kpi.objects.filter(code=serializer.validated_data['code']).exists():
            return Response(
                {"error": "Este KPI ya existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear el KPI
        kpi = serializer.save()
        return Response(
            {"message": f"KPI {kpi.name} creado exitosamente"}, 
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_KPI(request, kpi_id):
    """
    Vista disponible para el superusuario y administración.
    Actualiza un KPI existente.
    """
    
    kpi = get_object_or_404(Kpi, id=kpi_id)
    serializer = KpiSerializer(kpi, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": f"KPI {kpi.name} actualizado correctamente"}
        )
    
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_KPI(request, kpi_id):
    """
    Vista disponible solo para el superusuario.
    Elimina un KPI existente.
    """

    kpi = get_object_or_404(Kpi, id=kpi_id)
    nombre = kpi.name
    kpi.delete()
    
    return Response(
        {"message": f"KPI {nombre} eliminado correctamente"}
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_KPI_details(request, kpi_id):
    """
    Vista disponible para todos los usuarios, muestra detalles de un KPI.
    """
    kpi = get_object_or_404(Kpi, id=kpi_id)
    serializer = KpiSerializer(kpi)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_KPI_goal(request):
    """
    Vista para ver las metas de KPIs.
    """
    kpi_goals = KpiTarget.objects.all()
    serializer = KpiTargetSerializer(kpi_goals, many=True)
    return Response({"KPI Goals": serializer.data})

@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_KPI_goal(request, kpi_goal_id):
    """
    Edita una meta de KPI existente.
    Solo disponible para administradores y superusuarios.
    """
    
    kpi_goal = get_object_or_404(KpiTarget, id=kpi_goal_id)
    serializer = KpiTargetSerializer(kpi_goal, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": f"KPI Goal {kpi_goal.id} actualizado correctamente"}
        )
    
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_KPI_goal(request, kpi_goal_id):
    """
    Elimina una meta de KPI.
    Solo disponible para superusuarios.
    """
    
    kpi_goal = get_object_or_404(KpiTarget, id=kpi_goal_id)
    goal_id = kpi_goal.id
    kpi_goal.delete()
    
    return Response(
        {"message": f"KPI Goal {goal_id} eliminado correctamente"}
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_KPI_target(request):
    """
    Crea una nueva meta para un KPI.
    Solo disponible para superusuarios.
    """
    
    serializer = KpiTargetSerializer(data=request.data)
    if serializer.is_valid():
        # Verificar si ya existe un target similar
        if KpiTarget.objects.filter(
            kpi=serializer.validated_data['kpi'],
            period=serializer.validated_data['period']
        ).exists():
            return Response(
                {"error": "Este KPI Target ya existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear el KPI Target
        kpi_target = serializer.save()
        return Response(
            {"message": f"KPI Target {kpi_target.id} creado exitosamente"}, 
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calcular_kpi(request, kpi_name):
    """
    Calcula un KPI específico basado en datos reales de la base de datos
    Parámetros de query opcionales:
    - fecha_inicio: YYYY-MM-DD (por defecto: inicio del mes actual)
    - fecha_fin: YYYY-MM-DD (por defecto: fecha actual)
    - costo_hora: float (por defecto: calculado automáticamente)
    """
    try:
        # Obtener parámetros de fecha
        fecha_fin_str = request.GET.get('fecha_fin')
        fecha_inicio_str = request.GET.get('fecha_inicio')
        costo_hora_custom = request.GET.get('costo_hora')
        
        # Establecer fechas por defecto
        if fecha_fin_str:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        else:
            fecha_fin = datetime.date.today()
        
        if fecha_inicio_str:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        else:
            # Por defecto, inicio del mes actual
            fecha_inicio = fecha_fin.replace(day=1)
        
        # Validar que fecha_inicio <= fecha_fin
        if fecha_inicio > fecha_fin:
            return Response({
                'error': 'La fecha de inicio no puede ser posterior a la fecha de fin'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Recopilar datos
        costo_hora = float(costo_hora_custom) if costo_hora_custom else 250.0
        kpi_data = KPIDataCollector.collect_kpi_data(fecha_inicio, fecha_fin, costo_hora)
        
        # Calcular KPI específico
        calculator = KPI_Calculator()
        resultado = calculator.calculate_KPI(kpi_name, kpi_data)
        
        # Agregar información del período
        resultado['periodo'] = {
            'fecha_inicio': fecha_inicio.isoformat(),
            'fecha_fin': fecha_fin.isoformat(),
            'dias_totales': (fecha_fin - fecha_inicio).days + 1
        }
        
        return Response(resultado)
        
    except ValueError as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calcular_todos_kpis(request):
    """
    Calcula todos los KPIs disponibles
    Acepta los mismos parámetros que calcular_kpi
    """
    try:
        # Obtener parámetros (mismo código que calcular_kpi)
        fecha_fin_str = request.GET.get('fecha_fin')
        fecha_inicio_str = request.GET.get('fecha_inicio')
        costo_hora_custom = request.GET.get('costo_hora')
        
        if fecha_fin_str:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        else:
            fecha_fin = datetime.date.today()
        
        if fecha_inicio_str:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        else:
            fecha_inicio = fecha_fin.replace(day=1)
        
        if fecha_inicio > fecha_fin:
            return Response({
                'error': 'La fecha de inicio no puede ser posterior a la fecha de fin'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Recopilar datos
        costo_hora = float(costo_hora_custom) if costo_hora_custom else 250.0
        kpi_data = KPIDataCollector.collect_kpi_data(fecha_inicio, fecha_fin, costo_hora)
        
        # Calcular todos los KPIs
        calculator = KPI_Calculator()
        resultados = calculator.calculate_all_KPIs(kpi_data)
        
        # Agregar información del período a la respuesta
        response_data = {
            'periodo': {
                'fecha_inicio': fecha_inicio.isoformat(),
                'fecha_fin': fecha_fin.isoformat(),
                'dias_totales': (fecha_fin - fecha_inicio).days + 1
            },
            'resumen_datos': {
                'empleados_total': kpi_data.numero_empleados,
                'empleados_facturables': kpi_data.numero_empleados_facturables,
                'horas_planta_total': kpi_data.total_horas_planta,
                'horas_facturables': kpi_data.total_horas_facturables,
                'horas_facturadas': kpi_data.total_horas_facturadas,
                'ganancia_total': kpi_data.ganancia_total,
                'ingresos_directos': kpi_data.ingresos_directos,
                'ingresos_indirectos': kpi_data.ingresos_indirectos
            },
            'kpis': resultados
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response({
            'error': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
