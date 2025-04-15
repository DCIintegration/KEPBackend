from django.contrib import admin

from apps.proyectos.models import AsignacionProyecto, Proyecto

# Register your models here.
admin.site.register(Proyecto)
admin.site.register(AsignacionProyecto)