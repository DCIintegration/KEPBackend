from django.contrib import admin
from .models import Proyecto, AsignacionProyecto, RegistroHoras



admin.site.register(Proyecto)
admin.site.register(AsignacionProyecto)
admin.site.site_header = "KEP Proyectos Admin"
admin.site.site_title = "KEP Proyectos Admin"
admin.site.index_title = "Administración de Proyectos KEP"
admin.site.register(RegistroHoras)  # Asegúrate de importar RegistroHoras si lo necesitas