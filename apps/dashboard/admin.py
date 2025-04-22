from django.contrib import admin
from .models import KpiInputData, KpiTarget, Kpi

# Register your models here.
admin.site.register(KpiInputData)
admin.site.register(Kpi)
admin.site.register(KpiTarget)