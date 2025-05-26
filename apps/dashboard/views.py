from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.dashboard.models import Kpi, KpiTarget
from .serializers import KpiSerializer, KpiTargetSerializer
from apps.custom_auth.models import Empleado
from .utils import KPI_Calculator, KPIData
from apps.custom_auth.utils import FinantialInformation


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
    empleados = Empleado.objects.all()
    empleados_facturables = FinantialInformation.empleados_facturables()

    kpi_data = KPIData(
        total_horas_facturables = empleados_facturables * 8.5 * 22,  
        total_horas_facturadas = empleados_facturables * 7.5 * 22,  
        costo_por_hora = 250, 
        ganancia_total = 300000, 
        numero_empleados = empleados.count(),
        numero_empleados_facturables = empleados_facturables,
        dias_trabajados = 22
    )

    try:
        resultado = KPI_Calculator().calculate_KPI(kpi_name.upper(), kpi_data)
        return Response({kpi_name.upper(): resultado})
    except ValueError as e:
        return Response({"error": str(e)}, status=400)