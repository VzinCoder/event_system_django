from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from events.models import Event
from django.contrib.auth import get_user_model

'''
Os comandos sql se encontra no arquivo models do app events
'''

class Registration(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmada'),
        ('pending', 'Pendente'),
        ('canceled', 'Cancelada'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    registration_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        unique_together = ('user', 'event')

    def clean(self):
        if self.event.registration_set.count() >= self.event.max_participants:
            raise ValidationError(f'O evento {self.event.name} atingiu o limite de participantes.')
        
