# Generated by Django 5.1.7 on 2025-03-25 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='nombre',
            field=models.CharField(default='User', max_length=30),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='custom_auth.departamento'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
