# Generated by Django 4.2.4 on 2023-08-31 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='image',
        ),
    ]
