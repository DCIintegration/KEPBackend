from rest_framework import serializers
from .models import KpiInputData

class CompanyKPISerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo CompanyKPI, incluyendo todos los campos.
    """
    class Meta:
        model = KpiInputData
        fields = '__all__'
        
    def to_representation(self, instance):
        """
        Personaliza la representación JSON para mejorar legibilidad.
        """
        rep = super().to_representation(instance)
        rep['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M:%S') if instance.created_at else None
        return rep
