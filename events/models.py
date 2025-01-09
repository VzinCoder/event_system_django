from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    max_participants = models.IntegerField()

    def clean(self):
        if timezone.is_naive(self.date):
            self.date = timezone.make_aware(self.date)
    
        if self.date < timezone.now():
            raise ValidationError("O evento não pode ser realizado no passado.")

"""
--Resetaa as tabelas:
DELETE FROM registrations_registration;
DELETE FROM events_event;
DELETE FROM registrations_participant;
DELETE FROM sqlite_sequence WHERE name IN ('events_event', 'registrations_participant', 'registrations_registration');

--Comando para criar um evento:
INSERT INTO events_event (name, description, location, date, max_participants)
VALUES ('Hackathon de Programação', 'Evento de programação para todos os níveis.', 'São Paulo', '2025-05-17 10:00:00', 100);

--Comando para criar um participante:
INSERT INTO registrations_participant (name, email, phone, birth_date)
VALUES ('João Silva', 'joao.silva@example.com', '(11) 12345-6789', '2000-05-17');

--Comando para criar uma inscrição (com referências às tabelas de Evento e Participante):
INSERT INTO registrations_registration (event_id, participant_id, registration_date, status)
VALUES (1, 1, '2025-05-10 12:00:00', 'pending');

--Comando para consultar todos os eventos:
SELECT * FROM events_event;

--Comando para consultar todos os participantes:
SELECT * FROM registrations_participant;

--Comando para consultar inscrições para um evento específico:
SELECT * FROM registrations_registration WHERE event_id = 1;

--Comando para consultar inscrições de um participante específico:
SELECT * FROM registrations_registration WHERE participant_id = 1;

--Comando para atualizar o status de uma inscrição:
UPDATE registrations_registration
SET status = 'confirmed'
WHERE id = 1;

--Comando para atualizar um evento (modificando o nome e a localização, por exemplo):
UPDATE events_event
SET name = 'Hackathon de Inteligência Artificial', location = 'Rio de Janeiro'
WHERE id = 1;

--Comando para atualizar um participante (modificando o email):
UPDATE registrations_participant
SET email = 'joao.silva.novo@example.com'
WHERE id = 1;

--Comando para deletar uma inscrição:
DELETE FROM registrations_registration
WHERE id = 1;

--Comando para deletar um participante:
DELETE FROM registrations_participant
WHERE id = 1;

--Comando para deletar um evento:
DELETE FROM events_event
WHERE id = 1;
"""