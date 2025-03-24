from collections import defaultdict
from django.db import models
from dashboard.excel_procesor import FileProcessor

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
        ('DB', 'Days Backlog (DB)'),
        ('DCH', 'Days Cash on Hand (DCH)'),
    ]
    
    KPI_TYPES = (
        ('number', 'Número'),
        ('percentage', 'Porcentaje'),
        ('currency', 'Moneda'),
        ('days', 'Días'),
    )
    
    code = models.CharField(max_length=10, choices=KPI_CHOICES, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    kpi_type = models.CharField(max_length=20, choices=KPI_TYPES)
    unit = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_code_display()} - {self.name}"

class KpiInputData(models.Model):
    """Datos de entrada necesarios para calcular los KPIs"""
    period = models.DateField(help_text="Fecha que representa el período (ej. 2023-05-01 para mayo 2023)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Campos de datos brutos
    raw_data_file = models.FileField(upload_to='kpi_raw_data/', null=True, blank=True)
    file_type = models.CharField(max_length=20, choices=[('total', 'Total'), ('mensual', 'Mensual')])
    
    # Campos calculados (podrían ser propiedades en lugar de campos de BD)
    total_horas_facturables = models.FloatField(null=True, blank=True, default=0)
    total_horas_planta = models.FloatField(null=True, blank=True, default=0)
    total_horas_facturadas = models.FloatField(null=True, blank=True, default=0)
    numero_empleados = models.IntegerField(null=True, blank=True, default=0) 
    numero_empleados_facturables = models.IntegerField(null=True, blank=True, default=0) #Informacion de administracion, lo que registra estuardo para cada empleado de su nomina
    dias_trabajados = models.IntegerField(null=True, blank=True, default=0)
    costo_por_hora = models.FloatField(null=True, blank=True, default=0) 
    ganancia_total = models.FloatField(null=True, blank=True, default=0)
    
    class Meta:
        verbose_name = "Datos de Entrada para KPIs"
        ordering = ['-period']
        unique_together = [['period', 'file_type']]
    
    def __str__(self):
        return f"Datos para {self.period.strftime('%Y-%m')} ({self.get_file_type_display()})"
    
    def save(self, *args, **kwargs):
        # Procesar el archivo si se ha subido uno nuevo
        if self.raw_data_file and not self.pk:
            self.process_raw_file()
        super().save(*args, **kwargs)
    
    def process_raw_file(self):
        """Procesa el archivo subido y extrae los datos"""
        processor = FileProcessor(
            log_function=lambda msg: print(msg),  # Puedes reemplazar con tu sistema de logging
            is_plant_task_function=lambda actividad: "planta" in actividad.lower()
        )
        
        # Diccionarios temporales para almacenar datos
        horas_por_ot = defaultdict(lambda: {"total": 0, "planta": 0})
        horas_mensuales_por_ot = defaultdict(lambda: {"total": 0, "planta": 0})
        info_por_ot = {}
        
        # Procesar el archivo
        file_path = self.raw_data_file.path
        processor.process_raw_data(
            file_path=file_path,
            file_type=self.file_type,
            horas_por_ot=horas_por_ot,
            horas_mensuales_por_ot=horas_mensuales_por_ot,
            info_por_ot=info_por_ot
        )
        
        # Calcular totales
        self.total_horas_facturables = sum(ot_data["total"] for ot_data in horas_por_ot.values()) #Las alimentara osmar 
        self.total_horas_planta = sum(ot_data["planta"] for ot_data in horas_por_ot.values()) # Las horas planta seran las horas reportadas en el excel

class CalculatedKpi(models.Model):
    """KPIs calculados a partir de los datos de entrada"""
    kpi = models.ForeignKey(Kpi, on_delete=models.CASCADE)
    input_data = models.ForeignKey(KpiInputData, on_delete=models.CASCADE, related_name='calculated_kpis')
    value = models.FloatField()
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "KPI Calculado"
        verbose_name_plural = "KPIs Calculados"
        ordering = ['kpi', 'input_data__period']
        unique_together = [['kpi', 'input_data']]
    
    def __str__(self):
        return f"{self.kpi.code} - {self.input_data.period}: {self.value}"

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