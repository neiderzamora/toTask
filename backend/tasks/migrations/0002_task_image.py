# Generated by Django 4.2.4 on 2023-08-31 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='image',
            field=models.ImageField(default='/toTask.jpg', upload_to='images/', verbose_name='Image'),
        ),
    ]
