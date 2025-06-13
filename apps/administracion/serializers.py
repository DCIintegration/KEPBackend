from rest_framework import serializers
from .models import  IngresoActividad

class IngresoActividadSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para mostrar las opciones legibles
    actividad_display = serializers.CharField(source='get_actividad_display', read_only=True)
    tipo_ingreso_display = serializers.CharField(source='get_tipo_ingreso_display', read_only=True)
    month_display = serializers.CharField(source='get_month_display', read_only=True)
    
    class Meta:
        model = IngresoActividad
        fields = [
            'id',  # Útil para identificación única
            'actividad',
            'actividad_display',  # Versión legible de la actividad
            'monto',
            'month',
            'month_display',  # Versión legible del mes
            'year',
            'tipo_ingreso',
            'tipo_ingreso_display',  # Versión legible del tipo de ingreso
        ]
        
    def validate_monto(self, value):
        """Validación personalizada para el monto"""
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a 0")
        return value
    
    def validate_year(self, value):
        """Validación personalizada para el año"""
        if value and (value < 2000 or value > 2100):
            raise serializers.ValidationError("El año debe estar entre 2000 y 2100")
        return value
    
    def validate(self, data):
        """Validación a nivel de objeto"""
        # Verificar que si se proporciona month, también se proporcione year
        if data.get('month') and not data.get('year'):
            raise serializers.ValidationError("Si especifica un mes, debe especificar también el año")
        
        return data


