from django.db import models

class Kpi(models.Model):
    """Definición de cada KPI con fórmulas específicas"""
    KPI_CHOICES = [
        ('ELDR', 'Earnings per Labor Dollar Rate (ELDR)'),
        ('RE', 'Revenue per Employee (RE)'),
        ('RBE', 'Revenue per Billable Employee (RBE)'),
        ('UBH', 'Utilization Billable Hours (UBH)'),
        ('UB', 'Utilization Benchmark (UB)'),
        ('LM', 'Labor Multiplier (LM)'),
        ('LMM', 'Labor Maximum Multiplier (LMM)'),
    ]
    
    code = models.CharField(max_length=10, choices=KPI_CHOICES, unique=True) 
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return f"{self.get_code_display()} "


class KpiTarget(models.Model):
    """Objetivos para cada KPI por período"""
    kpi = models.ForeignKey(Kpi, on_delete=models.CASCADE)
    period = models.DateField()
    target_value = models.FloatField()
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Objetivo de KPI"
        ordering = ['kpi', 'period']
        unique_together = [['kpi', 'period']]
    
    def __str__(self):
        return f"Objetivo {self.kpi.code} - {self.period}: {self.target_value}"
    
class KpiInputData(models.Model):

    """Datos de entrada necesarios para calcular los KPIs"""
    
    total_horas_planta = models.FloatField(null=True, blank=True, default=0)