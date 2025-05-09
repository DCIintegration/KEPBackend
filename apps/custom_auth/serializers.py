from rest_framework import serializers
from apps.custom_auth.models import Empleado
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Departamento

class EmpleadoSerializer(serializers.ModelSerializer):
    """
    Serializer para operaciones con empleados.
    """
    departamento = serializers.PrimaryKeyRelatedField(
        queryset=Departamento.objects.all(),
        required=False,
        allow_null=True
    )
    departamento_nombre = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Empleado
        fields = [
            'id', 'email', 'nombre', 'role', 'puesto', 
            'fecha_contratacion', 'activo', 'sueldo', 
            'departamento', 'departamento_nombre', 
            'profile_picture', 'facturable', 'password'
        ]
        extra_kwargs = {
            'profile_picture': {'read_only': True},
            'id': {'read_only': True},
        }
    
    def get_departamento_nombre(self, obj):
        """Retorna el nombre del departamento si existe."""
        return obj.departamento.nombre if obj.departamento else None
    
    def validate(self, data):
        """Validación personalizada para campos requeridos en la creación."""
        if self.context.get('request') and self.context['request'].method == 'POST':
            required_fields = ["email", "nombre", "role", "puesto", "fecha_contratacion", "sueldo"]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                raise serializers.ValidationError(
                    f"Faltan campos requeridos: {', '.join(missing_fields)}"
                )
        return data
    
    def create(self, validated_data):
        """
        Crea y devuelve un nuevo empleado con contraseña cifrada.
        """
        password = validated_data.pop('password', None)
        # Usar create_user en lugar de create para manejar adecuadamente el cifrado de contraseñas
        empleado = Empleado.objects.create_user(
            username=validated_data.pop('email').split('@')[0],  # Usar primera parte del email como username
            email=validated_data.get('email'),
            password=password,
            **validated_data
        )
        return empleado
    
    def update(self, instance, validated_data):
        """
        Método personalizado para actualizar un empleado.
        Actualiza solo los campos proporcionados en los datos.
        """
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Manejar la contraseña por separado
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para obtener tokens JWT con información adicional.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadir datos personalizados al token
        token['nombre'] = user.nombre
        token['email'] = user.email
        token['role'] = user.role
        token['puesto'] = user.puesto
        token['activo'] = user.activo
        token['facturable'] = user.facturable
        token['departamento'] = user.departamento.id if user.departamento else None

        return token

class EmpleadoRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para el registro de empleados con generación de tokens JWT.
    """
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()
    departamento = serializers.PrimaryKeyRelatedField(
        queryset=Departamento.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Empleado
        fields = [
            'id', 'email', 'nombre', 'role', 'puesto', 
            'fecha_contratacion', 'activo', 'sueldo', 
            'departamento', 'facturable', 'password', 'tokens'
        ]

    def get_tokens(self, user):
        """
        Genera tokens JWT para el usuario.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        """
        Crea un nuevo empleado con contraseña cifrada y genera tokens JWT.
        """
        password = validated_data.pop('password', None)
        username = validated_data.get('email', '').split('@')[0]  # Primera parte del email como username
        
        empleado = Empleado.objects.create_user(
            username=username,
            email=validated_data.pop('email', ''),
            password=password,
            **validated_data
        )
        return empleado

# También necesitamos mantener el LoginSerializer para compatibilidad con vistas existentes
class LoginSerializer(serializers.Serializer):
    """
    Serializer para el proceso de login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        """Valida que se hayan proporcionado email y password."""
        if not data.get('email') or not data.get('password'):
            raise serializers.ValidationError("Email y contraseña son obligatorios")
        return data