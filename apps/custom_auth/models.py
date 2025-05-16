from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class Departamento(models.Model):
    nombre = models.CharField(max_length=30)
    nomina_mensual = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    nombre_completo = models.CharField(max_length=30, default="User")
    puesto = models.CharField(max_length=100)
    fecha_contratacion = models.DateField(default=datetime.today)
    activo = models.BooleanField(default=True)
    sueldo = models.PositiveIntegerField(default=0)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre_completo


class CustomUser(AbstractUser):

    ROLES = [

    ]
    
    email = models.EmailField(unique=True)  
    username = models.CharField(max_length=30, unique=False, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email
