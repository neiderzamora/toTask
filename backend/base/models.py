from django.db import models
from django.utils import timezone
from users.models import CustomUser
import uuid

class Activities(models.Model):

    STATUS_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Aprovada','Aprovada'),
        ('Retrasada','Retrasada'),
        ('SinFinalizar', 'SinFinalizar'),
    )
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    name = models.CharField('nombre', max_length=100, blank=False)
    description = models.TextField('descripcion', max_length=255)
    assigned_resources = models.TextField('recursos asignados', max_length=255)
    date_created = models.DateTimeField('fecha de creacion', auto_now_add=True)
    date_start = models.DateTimeField('fecha de inicio', default=timezone.datetime(2023, 8, 25, 10, 0))
    date_finish = models.DateTimeField('fecha de finalización', default=timezone.datetime(2023, 8, 25, 10, 0))
    status = models.CharField('estado', choices=STATUS_CHOICES, max_length=20, default='Pendiente')

    def __str__(self):
        return self.name