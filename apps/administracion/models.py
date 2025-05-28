from django.db import models

class FinantialData(models.Model):
    """Modelo para almacenar datos financieros"""

    # Campos del modelo
    total_horas_facturadas = models.FloatField(null=True, blank=True, default=0)
    ganancia_total = models.FloatField(null=True, blank=True, default=0)
    month = models.CharField(max_length=12, null=True, blank=True, choices=[
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
    ])
    year = models.IntegerField(null=True, blank=True , choices=[(i, i) for i in range(2000, 2100)])

    class Meta:
        unique_together = ('month', 'year')

class IngresoActividad(models.Model):
    """Modelo para almacenar ingresos de actividades"""

    ACTS= [
        ('Envio', 'Envio'),
        ('Equipo', 'Equipo'),
        ('Ingenieria de Control', 'Ingenieria de Control'),
        ('PLC', 'OLC'),
        ('Reparacion Servidores', 'Reparacion Servidores'),
        ('Servicio Electrico', 'Servicio Electrico'),
        ('Servicio Redes', 'Servicio Redes'),
        ('Software (Licencias)', 'Software (Licencias)'),
        ('Tableros', 'Tableros'),
        ('Viaticos', 'Viaticos'),
        
        
    ]

    actividad = models.CharField(choices=ACTS, max_length=100)
    monto = models.FloatField()
    fecha = models.DateField()

    def __str__(self):
        return f"{self.actividad} - {self.monto} - {self.fecha}"
    
    class Meta:
        verbose_name_plural = "Ingresos de Actividades"

