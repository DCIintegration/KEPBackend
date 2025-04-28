from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from apps.custom_auth.models import Empleado
from .serializers import EmpleadoSerializer, EmpleadoUpdateSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Autentica a un usuario y devuelve tokens de acceso y refresco.
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if not user.activo:
                return Response(
                    {"error": "Tu cuenta está desactivada"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if not user.is_email_verified:
                return Response(
                    {"error": "Debes verificar tu correo"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "Inicio de sesión exitoso",
                "user": {
                    "nombre": user.nombre,
                    "role": user.role,
                    "email": user.email
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        
        return Response(
            {"error": "Credenciales incorrectas"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Invalida el token de refresco del usuario (Logout).
    """
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token is None:
            return Response({"error": "Se requiere token de refresco"}, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        token.blacklist()  # Requiere configuración del Blacklist app
        return Response({"message": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    """
    Crea un nuevo usuario (empleado).
    Solo disponible para superusuarios.
    """
    if not request.user.is_superuser:
        return Response(
            {"error": "No tienes permisos para crear usuarios"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = EmpleadoSerializer(data=request.data)
    if serializer.is_valid():
        # Validar si el usuario ya existe
        if Empleado.objects.filter(email=serializer.validated_data["email"]).exists():
            return Response(
                {"error": "El usuario ya existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear usuario
        serializer.save()
        return Response(
            {"message": f"Usuario {serializer.validated_data['nombre']} creado correctamente"}, 
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, empleado_id):
    """
    Elimina un usuario basado en su ID.
    Solo disponible para superusuarios.
    """
    if not request.user.is_superuser:
        return Response(
            {"error": "No tienes permisos para eliminar usuarios"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    empleado = get_object_or_404(Empleado, id=empleado_id)
    nombre = empleado.nombre
    empleado.delete()
    
    return Response(
        {"message": f"Usuario {nombre} eliminado correctamente"},
        status=status.HTTP_200_OK
    )

@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request, empleado_id):
    """
    Actualiza la información de un usuario.
    Solo disponible para superusuarios.
    """
    if not request.user.is_superuser:
        return Response(
            {"error": "No tienes permisos para actualizar usuarios"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    empleado = get_object_or_404(Empleado, id=empleado_id)
    serializer = EmpleadoUpdateSerializer(empleado, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": f"Usuario {empleado.nombre} actualizado correctamente"},
            status=status.HTTP_200_OK
        )
    
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_users(request):
    """
    Retorna la lista de todos los usuarios.
    Solo disponible para superusuarios.
    """
    if not request.user.is_superuser:
        return Response(
            {"error": "No tienes permisos para visualizar esta información"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    empleados = Empleado.objects.all()
    serializer = EmpleadoSerializer(empleados, many=True)
    
    return Response({"Empleados": serializer.data})

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Autentica a un usuario y lo conecta al sistema.
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if not user.activo:
                return Response(
                    {"error": "Tu cuenta está desactivada"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if not user.is_email_verified:
                return Response(
                    {"error": "Debes verificar tu correo"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            login(request, user)
            return Response({
                "message": "Inicio de sesión exitoso", 
                "user": {
                    "nombre": user.nombre, 
                    "role": user.role, 
                    "email": user.email
                }
            })
        
        return Response(
            {"error": "Credenciales incorrectas"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Cierra la sesión del usuario autenticado.
    """
    if request.user.is_authenticated:
        logout(request)
        return Response({"message": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)
    
    return Response({"error": "No hay sesión activa"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_user(request):
    """
    Retorna la información del usuario autenticado.
    """
    if request.user.is_authenticated:
        serializer = EmpleadoSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
    
    return Response({"error": "No hay sesión activa"}, status=status.HTTP_400_BAD_REQUEST)