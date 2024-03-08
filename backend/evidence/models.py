from django.db import models
from .models import *
from tasks.models import Task
from users.models import CustomUser
import uuid

class File(models.Model):
    evidence = models.ForeignKey('Evidence', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='archivos_entrega/', default='/toTask.jpg')

class Evidence(models.Model):
    STATUS_CHOICES = (
        ('enviado', 'Enviado'),
        ('noenviado', 'NoEnviado')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tasks', default=None)
    description = models.TextField('descripcion', max_length=255, blank=False)
    status = models.CharField('Estado', max_length=10, choices=STATUS_CHOICES, blank=False, default='noenviado')
    date_upload = models.DateTimeField('fecha y hora de subida', auto_now_add=True)
    files = models.ManyToManyField(File, related_name='evidences')

    def __str__(self):
        return self.description
