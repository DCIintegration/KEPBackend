from django.db import models
from custom_auth.models import Empleado

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

    empleados = models.ManyToManyField('Empleado', through='AsignacionProyecto')

    def __str__(self):
        return self.nombre

class AvanceProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tarea = models.CharField(max_length=50)
    horas_trabajadas = models.PositiveIntegerField(default=0)