from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from apps.custom_auth.models import Empleado, Departamento
from .serializers import EmpleadoSerializer, EmpleadoRegisterSerializer, CustomTokenObtainPairSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationView(generics.CreateAPIView):
    """
    Vista para el registro de empleados.
    """
    serializer_class = EmpleadoRegisterSerializer
    permission_classes = [IsAdminUser]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Empleado creado exitosamente',
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
    """
    Retorna el perfil del usuario autenticado.
    """
    serializer = EmpleadoSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request, custom_user_id):
    """
    Retorna un usuario específico si el solicitante es superusuario o administrador.
    """
    if not (request.user.is_superuser or request.user.role == 'administracion'):
        return Response({
            'status': 'error', 
            'message': 'No tienes permisos para ver esta información'
        }, status=status.HTTP_403_FORBIDDEN)
    
    user = get_object_or_404(Empleado, id=custom_user_id)
    serializer = EmpleadoSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listUsers(request):
    """
    Retorna la lista de todos los usuarios si el solicitante es superusuario o administrador.
    """
    if not (request.user.is_superuser or request.user.role == 'administracion'):
        return Response({
            'status': 'error', 
            'message': 'No tienes permisos para ver esta información'
        }, status=status.HTTP_403_FORBIDDEN)
    
    users = Empleado.objects.all()
    serializer = EmpleadoSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, custom_user_id):
    """
    Actualiza un usuario específico si el solicitante es superusuario o el mismo usuario.
    """
    user = get_object_or_404(Empleado, id=custom_user_id)
    
    # Verificar permisos
    if not (request.user.is_superuser or request.user.id == custom_user_id):
        return Response({
            'status': 'error', 
            'message': 'No tienes permisos para modificar este usuario'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = EmpleadoSerializer(user, data=request.data, partial=True)
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
    """
    Elimina un usuario si el solicitante es superusuario.
    """
    if not request.user.is_superuser:
        return Response({
            'status': 'error', 
            'message': 'No tienes permisos para eliminar usuarios'
        }, status=status.HTTP_403_FORBIDDEN)
    
    user = get_object_or_404(Empleado, id=custom_user_id)
    user.delete()
    
    return Response({
        'status': 'success',
        'message': 'Usuario eliminado correctamente'
    })

@api_view(['POST'])
def logoutUser(request):
    """
    Invalida el token de refresco del usuario actual (logout).
    """
    try:
        refresh_token = request.data.get("refresh")  # Usar paréntesis en lugar de corchetes
        
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