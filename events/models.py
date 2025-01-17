from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

class Event(models.Model):
    VISIBILITY_CHOICES = [
        (True, 'Público'),
        (False, 'Privado'),
    ]
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField()
    registration_start_date = models.DateTimeField()
    registration_end_date = models.DateTimeField()
    image = models.ImageField(upload_to='images',null=True,blank=True)  
    current_participants = models.PositiveIntegerField(default=0)
    max_participants = models.PositiveIntegerField(default=1)
    visibility = models.BooleanField(choices=VISIBILITY_CHOICES, default=True)

    def __str__(self):
        visibility = "Público" if self.visibility else "Privado"
        return (
            f"Nome: {self.name}\n"
            f"Descrição: {self.description}\n"
            f"Localização: {self.location}\n"
            f"Início do Evento: {self.event_start_date.strftime('%d/%m/%Y %H:%M')}\n"
            f"Término do Evento: {self.event_end_date.strftime('%d/%m/%Y %H:%M')}\n"
            f"Início das Inscrições: {self.registration_start_date.strftime('%d/%m/%Y %H:%M')}\n"
            f"Término das Inscrições: {self.registration_end_date.strftime('%d/%m/%Y %H:%M')}\n"
            f"Imagem: {self.image.url if self.image else 'Sem imagem'}\n"
            f"Participantes Atuais: {self.current_participants}\n"
            f"Máximo de Participantes: {self.max_participants}\n"
            f"Visibilidade: {visibility}"
        )

"""
--Reseta as tabelas:
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

"""
--Seed para eventos 

-- Evento 1
INSERT INTO events_event (name, description, location, date, max_participants)
VALUES ('Hackathon de Programação', 'Evento de programação para todos os níveis.', 'São Paulo', '2025-05-17 10:00:00', 100);

-- Evento 2
INSERT INTO events_event (name, description, location, date, max_participants)
VALUES ('Workshop de Inteligência Artificial', 'Workshop intensivo sobre AI para iniciantes e profissionais.', 'Rio de Janeiro', '2025-06-20 09:00:00', 50);

-- Evento 3
INSERT INTO events_event (name, description, location, date, max_participants)
VALUES ('Conferência de Tecnologia', 'Conferência sobre as últimas inovações em tecnologia e startups.', 'Belo Horizonte', '2025-08-10 14:00:00', 200);

-- Evento 4
INSERT INTO events_event (name, description, location, date, max_participants)
VALUES ('Festival de Inovação', 'Festival para apresentação de novos projetos e soluções criativas.', 'Salvador', '2025-09-25 11:00:00', 150);

-- Evento 5
INSERT INTO events_event (name, description, location, date, max_participants)
VALUES ('Maratona de Programação', 'Competição intensa de codificação em tempo real.', 'São Paulo', '2025-07-10 08:00:00', 250);

-- Evento 6
INSERT INTO events_event (name, description, location, date, max_participants)
VALUES ('Summit de Marketing Digital', 'Evento sobre as últimas tendências em marketing digital.', 'Rio de Janeiro', '2025-06-05 10:00:00', 300);

-- Evento 7
INSERT INTO events_event (name, description, location, date, max_participants)
VALUES ('Fórum de Startups', 'Discussão sobre as oportunidades e desafios para startups.', 'Brasília', '2025-09-15 09:00:00', 120);

-- Evento 8
INSERT INTO events_event (name, description, location, date, max_participants)
VALUES ('Expo de Inovação Tecnológica', 'Exposição de soluções inovadoras na área de tecnologia.', 'Curitiba', '2025-10-03 14:00:00', 200);

-- Evento 9
INSERT INTO events_event (name, description, location, date, max_participants)
VALUES ('Hackathon de Inteligência Artificial', 'Evento com foco em IA, envolvendo grandes empresas de tecnologia.', 'São Paulo', '2025-12-01 09:00:00', 150);

-- Evento 10
INSERT INTO events_event (name, description, location, date, max_participants)
VALUES ('Semana de Design e UX', 'Semana dedicada ao design de experiência do usuário.', 'Florianópolis', '2025-11-15 13:00:00', 80);

--Seed para participantes 

-- Participante 1
INSERT INTO registrations_participant (name, email, phone, birth_date)
VALUES ('João Silva', 'joao.silva@example.com', '(11) 12345-6789', '2000-05-17');

-- Participante 2
INSERT INTO registrations_participant (name, email, phone, birth_date)
VALUES ('Maria Oliveira', 'maria.oliveira@example.com', '(21) 98765-4321', '1998-09-25');

-- Participante 3
INSERT INTO registrations_participant (name, email, phone, birth_date)
VALUES ('Carlos Souza', 'carlos.souza@example.com', '(31) 12345-6789', '1995-12-02');

-- Participante 4
INSERT INTO registrations_participant (name, email, phone, birth_date)
VALUES ('Fernanda Almeida', 'fernanda.almeida@example.com', '(61) 98765-4321', '1997-07-10');

-- Participante 5
INSERT INTO registrations_participant (name, email, phone, birth_date)
VALUES ('Pedro Costa', 'pedro.costa@example.com', '(85) 99876-5432', '2001-03-15');

-- Participante 6
INSERT INTO registrations_participant (name, email, phone, birth_date)
VALUES ('Ana Martins', 'ana.martins@example.com', '(41) 99887-6543', '1993-01-20');

-- Participante 7
INSERT INTO registrations_participant (name, email, phone, birth_date)
VALUES ('Roberto Lima', 'roberto.lima@example.com', '(19) 98765-1234', '1988-10-12');

-- Participante 8
INSERT INTO registrations_participant (name, email, phone, birth_date)
VALUES ('Juliana Pereira', 'juliana.pereira@example.com', '(21) 97654-3210', '1990-02-28');

-- Participante 9
INSERT INTO registrations_participant (name, email, phone, birth_date)
VALUES ('Lucas Silva', 'lucas.silva@example.com', '(85) 99987-6543', '1994-11-10');

-- Participante 10
INSERT INTO registrations_participant (name, email, phone, birth_date)
VALUES ('Carla Souza', 'carla.souza@example.com', '(44) 99887-6543', '1999-06-14');

--Seed para inscrição

-- Inscrição 1 (João Silva para o Hackathon de Programação)
INSERT INTO registrations_registration (event_id, participant_id, registration_date, status)
VALUES (1, 1, '2025-05-10 12:00:00', 'pending');

-- Inscrição 2 (Maria Oliveira para o Workshop de IA)
INSERT INTO registrations_registration (event_id, participant_id, registration_date, status)
VALUES (2, 2, '2025-06-19 15:00:00', 'confirmed');

-- Inscrição 3 (Carlos Souza para a Conferência de Tecnologia)
INSERT INTO registrations_registration (event_id, participant_id, registration_date, status)
VALUES (3, 3, '2025-08-09 10:30:00', 'confirmed');

-- Inscrição 4 (Fernanda Almeida para o Festival de Inovação)
INSERT INTO registrations_registration (event_id, participant_id, registration_date, status)
VALUES (4, 4, '2025-09-20 16:00:00', 'pending');

-- Inscrição 5 (João Silva para o Workshop de IA)
INSERT INTO registrations_registration (event_id, participant_id, registration_date, status)
VALUES (2, 1, '2025-06-18 14:00:00', 'pending');

-- Inscrição 6 (Pedro Costa para o Hackathon de Inteligência Artificial)
INSERT INTO registrations_registration (event_id, participant_id, registration_date, status)
VALUES (9, 5, '2025-11-30 09:00:00', 'confirmed');

-- Inscrição 7 (Ana Martins para o Summit de Marketing Digital)
INSERT INTO registrations_registration (event_id, participant_id, registration_date, status)
VALUES (6, 6, '2025-06-04 14:00:00', 'confirmed');

-- Inscrição 8 (Roberto Lima para o Fórum de Startups)
INSERT INTO registrations_registration (event_id, participant_id, registration_date, status)
VALUES (7, 7, '2025-09-10 13:00:00', 'pending');

-- Inscrição 9 (Juliana Pereira para a Expo de Inovação Tecnológica)
INSERT INTO registrations_registration (event_id, participant_id, registration_date, status)
VALUES (8, 8, '2025-10-02 17:00:00', 'pending');

-- Inscrição 10 (Lucas Silva para o Festival de Inovação)
INSERT INTO registrations_registration (event_id, participant_id, registration_date, status)
VALUES (4, 9, '2025-09-18 10:00:00', 'confirmed');
"""