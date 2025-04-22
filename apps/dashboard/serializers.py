from rest_framework import serializers
from apps.dashboard.models import Kpi, KpiTarget, KpiInputData

class KpiInputDataSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo KpiInputData.
    """
    class Meta:
        model = KpiInputData
        fields = [
            'id', 'total_horas_facturables', 'total_horas_planta', 'total_horas_facturadas',
            'numero_empleados', 'numero_empleados_facturables', 'dias_trabajados',
            'costo_por_hora', 'ganancia_total', 'status'
        ]

class KpiSerializer(serializers.ModelSerializer):
    """
    Serializer básico para el modelo Kpi.
    """
    class Meta:
        model = Kpi
        fields = ['id', 'name', 'code', 'description', 'value', 'data']

class KpiDetailSerializer(serializers.ModelSerializer):
    """
    Serializer detallado para el modelo Kpi.
    Usado para mostrar información completa de un KPI.
    """
    data_details = KpiInputDataSerializer(source='data', read_only=True)
    
    class Meta:
        model = Kpi
        fields = ['id', 'name', 'code', 'description', 'value', 'data', 'data_details', 'created_at']
        # Se incluye la información de los datos de entrada del KPI

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

class KpiWithTargetsSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar un KPI con sus targets asociados.
    """
    targets = serializers.SerializerMethodField()
    data_details = KpiInputDataSerializer(source='data', read_only=True)
    
    class Meta:
        model = Kpi
        fields = ['id', 'name', 'code', 'description', 'value', 'data', 'data_details', 'targets']
    
    def get_targets(self, obj):
        """Retorna todos los targets asociados al KPI."""
        targets = KpiTarget.objects.filter(kpi=obj)
        return KpiTargetSerializer(targets, many=True).data