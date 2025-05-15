from rest_framework import serializers
from apps.dashboard.models import KpiInputData

from rest_framework import serializers
from .models import Proyecto, AsignacionProyecto
from apps.custom_auth.models import Empleado
from apps.custom_auth.serializers import EmpleadoSerializer



class AsignacionProyectoSerializer(serializers.ModelSerializer):
    empleado = EmpleadoSerializer(read_only=True)
    empleado_id = serializers.PrimaryKeyRelatedField(
        queryset=Empleado.objects.all(), source='empleado', write_only=True
    )
    proyecto_id = serializers.PrimaryKeyRelatedField(
        queryset=Proyecto.objects.all(), source='proyecto', write_only=True
    )

    class Meta:
        model = AsignacionProyecto
        fields = [
            'id', 'proyecto_id', 'empleado', 'empleado_id', 'rol',
            'fecha_inicio', 'fecha_fin', 'horas_asignadas', 'horas_reales',
            'es_facturable', 'costo_hora', 'tarifa_hora'
        ]

class ProyectoSerializer(serializers.ModelSerializer):
    asignaciones = AsignacionProyectoSerializer(many=True, read_only=True)

    class Meta:
        model = Proyecto
        fields = [
            'id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin_estimada',
            'fecha_fin_real', 'estado', 'presupuesto', 'asignaciones'
        ]