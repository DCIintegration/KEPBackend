from django.contrib import admin

from apps.custom_auth.models import CustomUser, Departamento, Empleado

# Register your models here.
admin.site.register(Empleado)
admin.site.register(Departamento)
admin.site.register(CustomUser)