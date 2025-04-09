from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.custom_auth.models import Departamento, Empleado
from .serializers import DepartamentoSerializer, EmpleadoResumidoSerializer, EmpleadoUpdateSerializer

def is_admin_or_superuser(user):
    """
    Función auxiliar para verificar si un usuario es administrador o superusuario.
    """
    return user.is_admin() or user.is_custom_superuser() or user.is_superuser

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_administrativo(request):
    """
    Vista principal del dashboard administrativo.
    Retorna la lista de departamentos.
    """
    if not is_admin_or_superuser(request.user):
        return Response(
            {"error": "No tienes permiso para ver esta información"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    

    departamentos = Departamento.objects.all()
    serializer = DepartamentoSerializer(departamentos, many=True)
    
    return Response({"departamentos": serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def departamento_detalles(request, departamento_id):
    """
    Retorna detalles de un departamento específico y sus empleados.
    """
    if not is_admin_or_superuser(request.user):
        return Response(
            {"error": "No tienes permiso para ver esta información"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    departamento = get_object_or_404(Departamento, id=departamento_id)
    
    # Obtener y serializar empleados del departamento

    empleados = departamento.empleados_departamento()
    empleados_serializer = EmpleadoResumidoSerializer(empleados, many=True)
    
    # Construir respuesta con detalles del departamento y empleados
    response_data = {
        "id": departamento.id,
        "nombre": departamento.nombre,
        "nomina_mensual": departamento.nomina_mensual,
        "empleados": empleados_serializer.data
    }
    
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def empleado_detalles(request, empleado_id):
    """
    Retorna detalles completos de un empleado específico.
    """
    if not is_admin_or_superuser(request.user):
        return Response(
            {"error": "No tienes permiso para ver esta información"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    empleado = get_object_or_404(Empleado, id=empleado_id)
    
    # Crear respuesta con detalles del empleado
    response_data = {
        "id": empleado.id,
        "nombre": empleado.nombre,
        "rol": empleado.role,
        "puesto": empleado.puesto,
        "fecha_contratacion": empleado.fecha_contratacion,
        "activo": empleado.activo,
        "sueldo": empleado.sueldo,
        "departamento": empleado.departamento.nombre if empleado.departamento else None,
        "email": empleado.email,
        "imagen_perfil": empleado.profile_picture.url if empleado.profile_picture else None,
        "facturable": empleado.facturable
    }
    
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def modificar_datos(request, empleado_id):
    """
    Actualiza los datos de un empleado específico.
    """
    if not is_admin_or_superuser(request.user):
        return Response(
            {"error": "No tienes permiso para modificar esta información"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    empleado = get_object_or_404(Empleado, id=empleado_id)
    

    serializer = EmpleadoUpdateSerializer(empleado, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": f"Usuario {empleado.nombre} actualizado correctamente"}
        )
    
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )