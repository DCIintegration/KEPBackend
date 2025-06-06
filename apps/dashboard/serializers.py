from rest_framework import serializers
from apps.dashboard.models import Kpi, KpiTarget, KpiInputData

class KpiInputDataSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo KpiInputData.
    """
    class Meta:
        model = KpiInputData
        fields = [
            'id','total_horas_planta'
        ]

class KpiSerializer(serializers.ModelSerializer):
    """
    Serializer básico para el modelo Kpi.
    """
    class Meta:
        model = Kpi
        fields = ['id',  'code', 'description']


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
        min_value = data.get('min_value')
        target_value = data.get('target_value')
        max_value = data.get('max_value')
        
        if min_value is not None and target_value is not None and min_value > target_value:
            raise serializers.ValidationError(
                "El valor mínimo no puede ser mayor que el valor objetivo"
            )
        
        if max_value is not None and target_value is not None and target_value > max_value:
            raise serializers.ValidationError(
                "El valor objetivo no puede ser mayor que el valor máximo"
            )
        
        return data

