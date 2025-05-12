from django.db import models

class FinantialData(models.Model):
    """Modelo para almacenar datos financieros"""

    # Campos del modelo
    total_horas_facturadas = models.FloatField(null=True, blank=True, default=0)
    ganancia_total = models.FloatField(null=True, blank=True, default=0)
    month = models.CharField(max_length=20, null=True, blank=True, choices=[
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


