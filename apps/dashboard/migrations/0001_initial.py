# Generated by Django 5.2 on 2025-04-15 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KpiInputData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_horas_facturables', models.FloatField(blank=True, default=0, null=True)),
                ('total_horas_planta', models.FloatField(blank=True, default=0, null=True)),
                ('total_horas_facturadas', models.FloatField(blank=True, default=0, null=True)),
                ('numero_empleados', models.IntegerField(blank=True, default=0, null=True)),
                ('numero_empleados_facturables', models.IntegerField(blank=True, default=0, null=True)),
                ('dias_trabajados', models.IntegerField(blank=True, default=0, null=True)),
                ('costo_por_hora', models.FloatField(blank=True, default=0, null=True)),
                ('ganancia_total', models.FloatField(blank=True, default=0, null=True)),
                ('status', models.CharField(choices=[('correcto', 'Correcto'), ('reportado', 'Reportado'), ('corregido', 'Corregido')], default='correcto', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Kpi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(choices=[('ELDR', 'Earnings per Labor Dollar Rate (ELDR)'), ('RE', 'Revenue per Employee (RE)'), ('RBE', 'Revenue per Billable Employee (RBE)'), ('UBH', 'Utilization Billable Hours (UBH)'), ('UB', 'Utilization Benchmark (UB)'), ('LM', 'Labor Multiplier (LM)'), ('LMM', 'Labor Maximum Multiplier (LMM)')], max_length=10, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('value', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('data', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dashboard.kpiinputdata')),
            ],
        ),
        migrations.CreateModel(
            name='KpiTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.DateField()),
                ('target_value', models.FloatField()),
                ('min_value', models.FloatField(blank=True, null=True)),
                ('max_value', models.FloatField(blank=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('kpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.kpi')),
            ],
            options={
                'verbose_name': 'Objetivo de KPI',
                'ordering': ['kpi', 'period'],
                'unique_together': {('kpi', 'period')},
            },
        ),
    ]
