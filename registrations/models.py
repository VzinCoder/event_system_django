import re
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from events.models import Event

'''
Os comandos sql se encontra no arquivo models do app events
'''

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField()

    def clean(self):
        if self.birth_date > timezone.now().date():
            raise ValidationError(f"A data de nascimento não pode ser no futuro.")
        phone_regex = r"^\(\d{2}\)\s?\d{4,5}-\d{4}$"  
        if not re.match(phone_regex, self.phone):
            raise ValidationError(f"O número de telefone não está no formato correto. Exemplo: (11) 12345-6789.")


class Registration(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmada'),
        ('pending', 'Pendente'),
        ('canceled', 'Cancelada'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def clean(self):
        if self.event.registration_set.count() >= self.event.max_participants:
            raise ValidationError(f'O evento {self.event.name} atingiu o limite de participantes.')
        
