# Generated by Django 5.2.1 on 2025-05-19 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_remove_customuser_info_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('sistemas', 'Sistemas'), ('proyectos', 'Proyectos'), ('espctador', 'Espectador')], default='espectador', max_length=50),
        ),
    ]
