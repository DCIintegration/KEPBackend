from rest_framework import serializers
from .models import FinantialData

class FinantialDataSerializer(serializers.ModelSerializer):

    class Meta:
        models = FinantialData
        fields = [
            "total_horas_facturadas", "ganancia_total", "month", "year"
        ]


