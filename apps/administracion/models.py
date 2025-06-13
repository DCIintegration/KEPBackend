from django.db import models

class IngresoActividad(models.Model):
    """Modelo para almacenar ingresos de actividades"""
    
    ACTS = [
        ('Envio', 'Envio'),
        ('Equipo', 'Equipo'),
        ('Ingenieria de Control', 'Ingenieria de Control'),
        ('PLC', 'PLC'),  # Corregido: era 'OLC'
        ('Reparacion Servidores', 'Reparacion Servidores'),
        ('Servicio Electrico', 'Servicio Electrico'),
        ('Servicio Redes', 'Servicio Redes'),
        ('Software (Licencias)', 'Software (Licencias)'),
        ('Tableros', 'Tableros'),
        ('Viaticos', 'Viaticos'),
    ]
    
    MONTHS = [
        ('Enero', 'Enero'),
        ('Febrero', 'Febrero'),
        ('Marzo', 'Marzo'),
        ('Abril', 'Abril'),
        ('Mayo', 'Mayo'),
        ('Junio', 'Junio'),
        ('Julio', 'Julio'),
        ('Agosto', 'Agosto'),
        ('Septiembre', 'Septiembre'),
        ('Octubre', 'Octubre'),
        ('Noviembre', 'Noviembre'),
        ('Diciembre', 'Diciembre')
    ]
    
    TIPO_INGRESO = [
        ('Indirecto', 'Indirecto'),
        ('Directo', 'Directo')
    ]
    
    # Campos del modelo
    actividad = models.CharField(choices=ACTS, max_length=100)
    monto = models.FloatField()
    month = models.CharField(
        max_length=12, 
        null=True, 
        blank=True, 
        choices=MONTHS
    )
    year = models.IntegerField(
        null=True, 
        blank=True, 
        choices=[(i, i) for i in range(2000, 2100)]
    )
    tipo_ingreso = models.CharField(
        max_length=50, 
        choices=TIPO_INGRESO,
        default='Directo'  # Corregido: era 'Drecto'
    )
    
    # Campos de timestamp (recomendados)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.actividad} - {self.monto} - {self.fecha}"
    
    class Meta:
        unique_together = ('month', 'year')
        verbose_name = "Ingreso de Actividad"
        verbose_name_plural = "Ingresos de Actividades"
        ordering = ['-fecha']