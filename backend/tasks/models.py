from django.db import models
from django.utils import timezone
from users.models import CustomUser
from subActivities.models import SubActivities
import uuid

class Task(models.Model):

    STATUS_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Aprovada','Aprovada'),
        ('Retrasada','Retrasada'),
        ('SinFinalizar', 'SinFinalizar'),
    )
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    subActivity = models.ForeignKey(SubActivities, related_name='tasks', on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(CustomUser, related_name='user', on_delete=models.CASCADE, default=None)
    user_staff = models.ForeignKey(CustomUser, related_name='user_staff', on_delete=models.CASCADE, default=None)
    name = models.CharField('nombre', max_length=100, blank=False)
    description = models.TextField('descripcion', max_length=255)
    percentage = models.DecimalField('Porcentaje', max_digits=5, decimal_places=2)
    assigned_resources = models.TextField('recursos asignados', max_length=255)
    date_created = models.DateTimeField('fecha de creacion', auto_now_add=True)
    date_start = models.DateTimeField('fecha de inicio', default=timezone.datetime(2023, 8, 25, 10, 0))
    date_finish = models.DateTimeField('fecha de finalización', default=timezone.datetime(2023, 8, 25, 10, 0))
    status = models.CharField('estado', choices=STATUS_CHOICES, max_length=20, default='Pendiente')

    def __str__(self):
        return self.name