# Generated by Django 4.2.4 on 2023-08-25 17:32

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('description', models.TextField(max_length=255, verbose_name='descripcion')),
                ('assigned_resources', models.TextField(max_length=255, verbose_name='recursos asignados')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='fecha de creacion')),
                ('date_start', models.DateTimeField(default=datetime.datetime(2023, 8, 25, 10, 0), verbose_name='fecha de inicio')),
                ('date_finish', models.DateTimeField(default=datetime.datetime(2023, 8, 25, 10, 0), verbose_name='fecha de finalización')),
                ('status', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aprovada', 'Aprovada'), ('Retrasada', 'Retrasada'), ('SinFinalizar', 'SinFinalizar')], default='Pendiente', max_length=20, verbose_name='estado')),
            ],
        ),
    ]
