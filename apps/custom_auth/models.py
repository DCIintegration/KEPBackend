from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class Departamento(models.Model):
    nombre = models.CharField(max_length=30)
    nomina_mensual = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.nombre
    
    def empleados_departamento(self):
        """Método para obtener empleados del departamento"""
        return self.empleado_set.all()
    
    def calcular_nomina_total(self):
        """Calcula la nómina total del departamento"""
        return sum(empleado.sueldo for empleado in self.empleado_set.filter(activo=True))

class Empleado(models.Model):
    nombre_completo = models.CharField(max_length=100, default="User")  
    puesto = models.CharField(max_length=100)
    fecha_contratacion = models.DateField(default=datetime.today)
    activo = models.BooleanField(default=True)
    sueldo = models.PositiveIntegerField(default=0)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre_completo

class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('sistemas', 'Sistemas'),
        ('proyectos', 'Proyectos'),
        ('espectador', 'Espectador'),  
    )
    
    email = models.EmailField(unique=True)  
    username = models.CharField(max_length=30, unique=False, null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLES, default="espectador")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"] 

    def __str__(self):
        return self.email