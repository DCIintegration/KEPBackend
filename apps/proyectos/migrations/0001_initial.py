# Generated by Django 5.2 on 2025-05-13 16:01

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('lider', 'Líder de Proyecto'), ('desarrollador', 'Desarrollador'), ('tester', 'Tester'), ('diseñador', 'Diseñador'), ('analista', 'Analista'), ('gerente', 'Gerente')], default='desarrollador', max_length=20)),
                ('fecha_inicio', models.DateField(default=django.utils.timezone.now)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('horas_asignadas', models.PositiveIntegerField(default=0)),
                ('horas_reales', models.PositiveIntegerField(default=0)),
                ('es_facturable', models.BooleanField(default=True)),
                ('costo_hora', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('tarifa_hora', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignaciones_proyectos', to='custom_auth.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin_estimada', models.DateField()),
                ('fecha_fin_real', models.DateField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('planificacion', 'En Planificación'), ('desarrollo', 'En Desarrollo'), ('testing', 'En Testing'), ('completado', 'Completado'), ('suspendido', 'Suspendido')], default='planificacion', max_length=20)),
                ('presupuesto', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('empleados', models.ManyToManyField(through='proyectos.AsignacionProyecto', to='custom_auth.empleado')),
            ],
        ),
        migrations.AddField(
            model_name='asignacionproyecto',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignaciones', to='proyectos.proyecto'),
        ),
    ]
