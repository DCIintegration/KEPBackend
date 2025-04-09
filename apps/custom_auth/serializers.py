from rest_framework import serializers
from apps.custom_auth.models import Empleado, Departamento

class DepartamentoRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Campo personalizado para manejar la relación con departamentos.
    Permite asignar None al departamento.
    """
    def to_internal_value(self, data):
        if data in (None, '', 'null'):
            return None
        return super().to_internal_value(data)

class EmpleadoSerializer(serializers.ModelSerializer):
    """
    Serializer para operaciones con empleados.
    """
    departamento = DepartamentoRelatedField(
        queryset=Departamento.objects.all(),
        required=False,
        allow_null=True
    )
    departamento_nombre = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Empleado
        fields = [
            'id', 'email', 'nombre', 'role', 'puesto', 
            'fecha_contratacion', 'activo', 'sueldo', 
            'departamento', 'departamento_nombre', 
            'profile_picture', 'facturable'
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

class EmpleadoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar datos de empleados.
    """
    departamento = DepartamentoRelatedField(
        queryset=Departamento.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Empleado
        fields = [
            'nombre', 'role', 'puesto', 'fecha_contratacion',
            'activo', 'sueldo', 'departamento', 'facturable'
        ]
    
    def update(self, instance, validated_data):
        """
        Método personalizado de actualización.
        Actualiza solo los campos proporcionados.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

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