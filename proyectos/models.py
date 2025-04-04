from django.db import models
from custom_auth.models import Empleado
from django.utils import timezone


class Proyecto(models.Model):
    ESTADO_CHOICES = [
        ('planificacion', 'En Planificación'),
        ('desarrollo', 'En Desarrollo'),
        ('testing', 'En Testing'),
        ('completado', 'Completado'),
        ('suspendido', 'Suspendido'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField()
    fecha_fin_real = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='planificacion')
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    empleados = models.ManyToManyField(Empleado, through='AsignacionProyecto')

    def __str__(self):
        return self.nombre


class AsignacionProyecto(models.Model):
    ROL_CHOICES = [
        ('lider', 'Líder de Proyecto'),
        ('desarrollador', 'Desarrollador'),
        ('tester', 'Tester'),
        ('diseñador', 'Diseñador'),
        ('analista', 'Analista'),
        ('gerente', 'Gerente'),
    ]

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='asignaciones')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='asignaciones_proyectos')
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='desarrollador')
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)
    horas_asignadas = models.PositiveIntegerField(default=0)
    horas_reales = models.PositiveIntegerField(default=0)
    es_facturable = models.BooleanField(default=True)
    costo_hora = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    tarifa_hora = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)


