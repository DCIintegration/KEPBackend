from rest_framework import serializers
from .models import FinantialData, IngresoActividad

class FinantialDataSerializer(serializers.ModelSerializer):

    class Meta:
        models = FinantialData
        fields = [
            "total_horas_facturadas", "ganancia_total", "month", "year"
        ]

class IngresoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngresoActividad
        fields = ['actividad', 'monto', 'fecha']
        read_only_fields = ['fecha']  # Fecha se asigna automáticamente al crear el registro
