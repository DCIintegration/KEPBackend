from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Departamento(models.Model):
    nombre = models.CharField(max_length=30)
    nomina_mensual = models.PositiveIntegerField(null=True, blank=True)

    def calcular_nomina(self):
        return sum(empleado.sueldo for empleado in self.empleado_set.all())
    
    def empleados_departamento(self):
        return self.empleado_set.count()

    def save(self, *args, **kwargs):
        if self.pk:
            self.nomina_mensual = self.calcular_nomina()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.nombre


#Separar usuarios de empleados
class Empleado(models.Model):
    class Roles(models.TextChoices):
        PROYECTOS = 'proyectos', 'Proyectos'
        INGENIERIA = 'ingenieria', 'Ingeniería'
        ADMINISTRACION = 'administracion', 'Administración'
        GERENCIA = 'gerencia', 'Gerencia'
        SUPERUSUARIO = 'superusuario', 'Superusuario'

    nombre = models.CharField(max_length=30, default="User")
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.INGENIERIA)
    puesto = models.CharField(max_length=100)
    fecha_contratacion = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))
    activo = models.BooleanField(default=True)
    sueldo = models.PositiveIntegerField(default=0)
    departamento = models.ForeignKey('Departamento', on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    facturable = models.BooleanField(default=False)

    

    def __str__(self):
        return self.nombre  # Muestra nombre en lugar de first_name/last_name

    def is_admin(self):
        return self.role == self.Roles.ADMINISTRACION

    def is_gerente(self):
        return self.role == self.Roles.GERENCIA

    def is_custom_superuser(self):
        return self.role == self.Roles.SUPERUSUARIO

    def is_proyectos(self):
        return self.role == self.Roles.PROYECTOS
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    info = models.OneToOneField(Empleado, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Solo incluye campos que están en este modelo

    def __str__(self):
        return self.email
