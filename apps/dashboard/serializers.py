from rest_framework import serializers
from apps.dashboard.models import Kpi, KpiTarget

class KpiSerializer(serializers.ModelSerializer):
    """
    Serializer básico para el modelo Kpi.
    """
    class Meta:
        model = Kpi
        fields = ['id', 'name', 'code', 'description', 'kpi_type', 'unit']

class KpiDetailSerializer(serializers.ModelSerializer):
    """
    Serializer detallado para el modelo Kpi.
    Usado para mostrar información completa de un KPI.
    """
    class Meta:
        model = Kpi
        fields = ['id', 'name', 'code', 'description', 'kpi_type', 'unit']
        # Se puede expandir con campos adicionales o relaciones en el futuro

class KpiTargetSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo KpiTarget.
    """
    kpi_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = KpiTarget
        fields = ['id', 'kpi', 'kpi_name', 'period', 'target_value', 'min_value', 'max_value']
        extra_kwargs = {
            'id': {'read_only': True},
        }
    
    def get_kpi_name(self, obj):
        """Retorna el nombre del KPI asociado."""
        return obj.kpi.name if obj.kpi else None
    
    def validate(self, data):
        """
        Validación personalizada para los valores del target.
        Asegura que min_value <= target_value <= max_value.
        """
        min_value = data.get('min_value', 0)
        target_value = data.get('target_value', 0)
        max_value = data.get('max_value', 0)
        
        if min_value > target_value:
            raise serializers.ValidationError(
                "El valor mínimo no puede ser mayor que el valor objetivo"
            )
        
        if target_value > max_value:
            raise serializers.ValidationError(
                "El valor objetivo no puede ser mayor que el valor máximo"
            )
        
        return data

class KpiWithTargetsSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar un KPI con sus targets asociados.
    """
    targets = serializers.SerializerMethodField()
    
    class Meta:
        model = Kpi
        fields = ['id', 'name', 'code', 'description', 'kpi_type', 'unit', 'targets']
    
    def get_targets(self, obj):
        """Retorna todos los targets asociados al KPI."""
        targets = KpiTarget.objects.filter(kpi=obj)
        return KpiTargetSerializer(targets, many=True).data