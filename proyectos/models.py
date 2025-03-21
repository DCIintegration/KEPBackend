from django.db import models
from custom_auth.models import Empleado
from dashboard.models import Proyecto

# Create your models here.
class AvanceProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tarea = models.CharField(max_length=50)
    horas_trabajadas = models.PositiveIntegerField(default=0)