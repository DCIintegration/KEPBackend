from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import FinantialInformation
from apps.custom_auth.models import CustomUser, Empleado, Departamento
from .serializers import EmpleadoSerializer, CustomUserRegisterSerializer, DepartamentoSerializer


"""-------- ENDPOINTS PARA USUARIOS ----------"""

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = CustomUserRegisterSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Usuario creado exitosamente',
                'user': serializer.data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    serializer = EmpleadoSerializer(request.user.info)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request, custom_user_id):
    user = get_object_or_404(CustomUser, id=custom_user_id)

    if not request.user.is_superuser:
        return Response({
            'status': 'error',
            'message': 'No tienes permisos para ver esta información'
        }, status=status.HTTP_403_FORBIDDEN)

    serializer = EmpleadoSerializer(user.info)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listUsers(request):
    if not request.user.is_superuser:
        return Response({
            'status': 'error',
            'message': 'No tienes permisos para ver esta información'
        }, status=status.HTTP_403_FORBIDDEN)

    users = CustomUser.objects.all()
    data = [EmpleadoSerializer(user.info).data for user in users if user.info]
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, custom_user_id):
    user = get_object_or_404(CustomUser, id=custom_user_id)

    if not (request.user.is_superuser or request.user.id == user.id):
        return Response({
            'status': 'error',
            'message': 'No tienes permisos para modificar este usuario'
        }, status=status.HTTP_403_FORBIDDEN)

    serializer = EmpleadoSerializer(user.info, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 'success',
            'message': 'Usuario actualizado correctamente',
            'user': serializer.data
        })

    return Response({
        'status': 'error',
        'message': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request, custom_user_id):
    if not request.user.is_superuser:
        return Response({
            'status': 'error',
            'message': 'No tienes permisos para eliminar usuarios'
        }, status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(CustomUser, id=custom_user_id)
    user.delete()

    return Response({
        'status': 'success',
        'message': 'Usuario eliminado correctamente'
    })


@api_view(['POST'])
def logoutUser(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({
                'status': 'error',
                'message': 'Token de refresco no proporcionado'
            }, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({
            'status': 'success',
            'message': 'Sesión cerrada correctamente'
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


"""-------- ENDPOINTS PARA EMPLEADOS ----------"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listEmployees(request):
    empleados = Empleado.objects.all()
    serializer = EmpleadoSerializer(empleados, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employeeDetails(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    response_data = {
        "id": empleado.id,
        "nombre completo": empleado.nombre_completo,
        "puesto": empleado.puesto,
        "fecha_contratacion": empleado.fecha_contratacion,
        "activo": empleado.activo,
        "sueldo": empleado.sueldo,
        "departamento": empleado.departamento.nombre if empleado.departamento else None,
        "email": empleado.email,
    }
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createEmployee(request):
    serializer = EmpleadoSerializer(data=request.data)
    if serializer.is_valid():
        empleado = serializer.save()
        return Response({
            "status": "success",
            "message": "Empleado creado exitosamente",
            "empleado": serializer.data
        }, status=201)
    return Response({
        "status": "error",
        "message": serializer.errors
    }, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateEmployee(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    serializer = EmpleadoSerializer(empleado, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "message": "Empleado actualizado correctamente",
            "empleado": serializer.data
        })
    return Response({
        "status": "error",
        "message": serializer.errors
    }, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteEmployee(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    empleado.delete()
    return Response({
        "status": "success",
        "message": "Empleado eliminado correctamente"
    })


"""-------- ENDPOINTS PARA DEPARTAMENTOS ----------"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listDepartment(request):
    departamentos = Departamento.objects.all()
    serializer = DepartamentoSerializer(departamentos, many=True)
    return Response({"departamentos": serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def departmentDetails(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    empleados = departamento.empleados_departamento()
    empleados_serializer = EmpleadoSerializer(empleados, many=True)
    response_data = {
        "id": departamento.id,
        "nombre": departamento.nombre,
        "nomina_mensual": departamento.nomina_mensual,
        "empleados": empleados_serializer.data
    }
    return Response(response_data)


"""-------- ENDPOINTS PARA INFORMACION PARA KPI ----------"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nominaDepartamento(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    empleados = Empleado.objects.filter(departamento=departamento)
    total_nomina = FinantialInformation.calcular_nomina_mensual(empleados, departamento)
    return Response({
        'departamento': departamento.nombre,
        'nomina_mensual': total_nomina
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def infoFinancieraGlobal(request):
    empleados = Empleado.objects.all()
    data = {
        'facturables': FinantialInformation.empleados_facturables(empleados),
        'horas_facturables': FinantialInformation.horas_facturables(empleados),
        'horas_planta': FinantialInformation.horas_plantas(empleados),
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEmployeeSalary(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    return Response({
        'empleado': empleado.nombre_completo,
        'sueldo': empleado.sueldo
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDepartmentSalary(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    empleados = Empleado.objects.filter(departamento=departamento)
    total_nomina = FinantialInformation.calcular_nomina_mensual(empleados, departamento)
    return Response({
        'departamento': departamento.nombre,
        'nomina_mensual': total_nomina
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def updateEmployeeSalary(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    nuevo_sueldo = request.data.get('sueldo')

    if nuevo_sueldo is None:
        return Response({
            'status': 'error',
            'message': 'Sueldo no proporcionado'
        }, status=status.HTTP_400_BAD_REQUEST)

    empleado.sueldo = nuevo_sueldo
    empleado.save()

    return Response({
        'status': 'success',
        'message': 'Sueldo actualizado correctamente',
        'empleado': EmpleadoSerializer(empleado).data
    })