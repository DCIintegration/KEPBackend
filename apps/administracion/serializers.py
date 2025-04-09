from rest_framework import serializers
from apps.custom_auth.models import Departamento, Empleado

class DepartamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para información básica de departamentos.
    """
    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'nomina_mensual']

class EmpleadoResumidoSerializer(serializers.ModelSerializer):
    """
    Serializer para información resumida de empleados.
    Usado principalmente para listar empleados dentro de un departamento.
    """
    class Meta:
        model = Empleado
        fields = ['id', 'nombre', 'puesto', 'sueldo']

class EmpleadoDetalleSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar información detallada de un empleado.
    """
    departamento = serializers.SerializerMethodField()
    imagen_perfil = serializers.SerializerMethodField()
    
    class Meta:
        model = Empleado
        fields = [
            'id', 'nombre', 'rol', 'puesto', 'fecha_contratacion',
            'activo', 'sueldo', 'departamento', 'email', 
            'imagen_perfil', 'facturable'
        ]
    
    def get_departamento(self, obj):
        """Retorna el nombre del departamento si existe."""
        return obj.departamento.nombre if obj.departamento else None
    
    def get_imagen_perfil(self, obj):
        """Retorna la URL de la imagen de perfil si existe."""
        return obj.profile_picture.url if obj.profile_picture else None

class EmpleadoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar datos de un empleado.
    """
    departamento = serializers.PrimaryKeyRelatedField(
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
        Método personalizado para actualizar un empleado.
        Actualiza solo los campos proporcionados en los datos.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance