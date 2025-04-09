from rest_framework import serializers
from apps.dashboard.models import KpiInputData

class KpiInputDataSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo KpiInputData.
    Utilizado para listar logs y crear/actualizar registros.
    """
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = KpiInputData
        fields = [
            'id', 'created_at', 'period', 'file_type', 'status',
            'total_horas_facturables', 'total_horas_planta', 'total_horas_facturadas',
            'numero_empleados', 'numero_empleados_facturables', 'dias_trabajados',
            'costo_por_hora', 'ganancia_total'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        """
        Validación personalizada para asegurar coherencia en los datos.
        """
        # Validar que los empleados facturables no excedan el total de empleados
        if 'numero_empleados' in data and 'numero_empleados_facturables' in data:
            if data['numero_empleados_facturables'] > data['numero_empleados']:
                raise serializers.ValidationError(
                    "El número de empleados facturables no puede ser mayor que el número total de empleados"
                )
        
        # Validar que las horas facturadas no excedan las facturables
        if 'total_horas_facturables' in data and 'total_horas_facturadas' in data:
            if data['total_horas_facturadas'] > data['total_horas_facturables']:
                raise serializers.ValidationError(
                    "El total de horas facturadas no puede ser mayor que el total de horas facturables"
                )
        
        return data

class CompanyKPISerializer(serializers.ModelSerializer):
    """
    Serializer detallado para mostrar información completa de un log de KPI.
    Incluye campos calculados y estadísticas derivadas.
    """
    porcentaje_facturacion = serializers.SerializerMethodField()
    porcentaje_empleados_facturables = serializers.SerializerMethodField()
    promedio_horas_por_empleado = serializers.SerializerMethodField()
    created_at_formatted = serializers.SerializerMethodField()
    periodo_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = KpiInputData
        fields = [
            'id', 'created_at', 'created_at_formatted', 'period', 'periodo_formatted',
            'file_type', 'status', 'total_horas_facturables', 'total_horas_planta',
            'total_horas_facturadas', 'numero_empleados', 'numero_empleados_facturables',
            'dias_trabajados', 'costo_por_hora', 'ganancia_total',
            'porcentaje_facturacion', 'porcentaje_empleados_facturables',
            'promedio_horas_por_empleado'
        ]
    
    def get_porcentaje_facturacion(self, obj):
        """
        Calcula el porcentaje de horas facturadas respecto a las facturables.
        """
        if obj.total_horas_facturables and obj.total_horas_facturables > 0:
            return round((obj.total_horas_facturadas / obj.total_horas_facturables) * 100, 2)
        return 0
    
    def get_porcentaje_empleados_facturables(self, obj):
        """
        Calcula el porcentaje de empleados facturables respecto al total.
        """
        if obj.numero_empleados and obj.numero_empleados > 0:
            return round((obj.numero_empleados_facturables / obj.numero_empleados) * 100, 2)
        return 0
    
    def get_promedio_horas_por_empleado(self, obj):
        """
        Calcula el promedio de horas trabajadas por empleado.
        """
        if obj.numero_empleados and obj.numero_empleados > 0:
            return round(obj.total_horas_planta / obj.numero_empleados, 2)
        return 0
    
    def get_created_at_formatted(self, obj):
        """
        Formatea la fecha de creación en un formato legible.
        """
        if obj.created_at:
            return obj.created_at.strftime('%d/%m/%Y %H:%M')
        return None
    
    def get_periodo_formatted(self, obj):
        """
        Formatea el periodo en un formato legible.
        """
        if obj.period:
            return obj.period.strftime('%B %Y')
        return None