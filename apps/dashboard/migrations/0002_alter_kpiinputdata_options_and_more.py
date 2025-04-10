# Generated by Django 5.2 on 2025-04-04 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kpiinputdata',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='kpiinputdata',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='kpi',
            name='kpi_type',
        ),
        migrations.RemoveField(
            model_name='kpi',
            name='unit',
        ),
        migrations.AddField(
            model_name='kpi',
            name='data',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dashboard.kpiinputdata'),
        ),
        migrations.AddField(
            model_name='kpi',
            name='value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='kpiinputdata',
            name='status',
            field=models.CharField(choices=[('correcto', 'Correcto'), ('reportado', 'Reportado'), ('corregido', 'Corregido')], default='correcto', max_length=20),
        ),
        migrations.AlterField(
            model_name='kpi',
            name='code',
            field=models.CharField(choices=[('ELDR', 'Earnings per Labor Dollar Rate (ELDR)'), ('RE', 'Revenue per Employee (RE)'), ('RBE', 'Revenue per Billable Employee (RBE)'), ('UBH', 'Utilization Billable Hours (UBH)'), ('UB', 'Utilization Benchmark (UB)'), ('LM', 'Labor Multiplier (LM)'), ('LMM', 'Labor Maximum Multiplier (LMM)')], max_length=10, unique=True),
        ),
        migrations.DeleteModel(
            name='CalculatedKpi',
        ),
        migrations.RemoveField(
            model_name='kpiinputdata',
            name='file_type',
        ),
        migrations.RemoveField(
            model_name='kpiinputdata',
            name='period',
        ),
        migrations.RemoveField(
            model_name='kpiinputdata',
            name='raw_data_file',
        ),
    ]
