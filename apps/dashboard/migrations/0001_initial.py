# Generated by Django 5.2 on 2025-05-13 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kpi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(choices=[('ELDR', 'Earnings per Labor Dollar Rate (ELDR)'), ('RE', 'Revenue per Employee (RE)'), ('RBE', 'Revenue per Billable Employee (RBE)'), ('UBH', 'Utilization Billable Hours (UBH)'), ('UB', 'Utilization Benchmark (UB)'), ('LM', 'Labor Multiplier (LM)'), ('LMM', 'Labor Maximum Multiplier (LMM)')], max_length=10, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='KpiInputData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_horas_planta', models.FloatField(blank=True, default=0, null=True)),
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
