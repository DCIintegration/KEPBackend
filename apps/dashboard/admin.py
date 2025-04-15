from django.contrib import admin

from apps.dashboard.models import Kpi, KpiInputData, KpiTarget

# Register your models here.
admin.site.register(KpiInputData)
admin.site.register(Kpi)
admin.site.register(KpiTarget)