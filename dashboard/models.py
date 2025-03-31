from django.db import models

class KpiInputData(models.Model):
    """Datos de entrada necesarios para calcular los KPIs"""
    created_at = models.DateTimeField(auto_now_add=True)
    
    total_horas_facturables = models.FloatField(null=True, blank=True, default=0)
    total_horas_planta = models.FloatField(null=True, blank=True, default=0)
    total_horas_facturadas = models.FloatField(null=True, blank=True, default=0)
    numero_empleados = models.IntegerField(null=True, blank=True, default=0) 
    numero_empleados_facturables = models.IntegerField(null=True, blank=True, default=0)
    dias_trabajados = models.IntegerField(null=True, blank=True, default=0)
    costo_por_hora = models.FloatField(null=True, blank=True, default=0) 
    ganancia_total = models.FloatField(null=True, blank=True, default=0)

class KPI_Calculator:
    @staticmethod
    def ELDR(kpi_data):
        return kpi_data.total_horas_facturables * kpi_data.costo_por_hora

    @staticmethod
    def RE(kpi_data):
        return kpi_data.ganancia_total / kpi_data.numero_empleados

    @staticmethod
    def RBE(kpi_data):
        return kpi_data.ganancia_total / kpi_data.numero_empleados_facturables

    @staticmethod
    def UBH(kpi_data):
        total_horas = ((kpi_data.numero_empleados_facturables * 8.5) * kpi_data.numero_empleados_facturables) * kpi_data.dias_trabajados
        return kpi_data.total_horas_facturadas / total_horas

    @staticmethod
    def UB(kpi_data):
        total_horas = ((kpi_data.numero_empleados_facturables * 8.5) * kpi_data.numero_empleados_facturables) * kpi_data.dias_trabajados
        return kpi_data.total_horas_facturables / total_horas

    @staticmethod
    def LM(kpi_data):
        return kpi_data.ganancia_total / kpi_data.costo_por_hora

    @staticmethod
    def LMM(kpi_data):
        return 8.5 * kpi_data.numero_empleados_facturables

    def calculate_KPI(self, kpi_name, kpi_data):
        kpi_methods = {method: getattr(self, method) for method in dir(self) if callable(getattr(self, method)) and not method.startswith("_")}
        
        if kpi_name in kpi_methods:
            return kpi_methods[kpi_name](kpi_data)
        else:
            raise ValueError("KPI no encontrado")

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
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    data = models.ForeignKey(KpiInputData, on_delete=models.CASCADE)
    value = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_value(self):
        calculator = KPI_Calculator()
        self.value = calculator.calculate_KPI(self.code, self.data)
        self.save()
    
    def __str__(self):
        return f"{self.get_code_display()} - {self.name}"


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