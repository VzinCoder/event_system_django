from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from events.models import Event
from .models import Registration
from django.db import DatabaseError, transaction
from django.contrib.messages import get_messages


class RegistrationModelTest(TestCase):
    def setUp(self):
        # Cria um usuário e um evento para usar nos testes
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.event = Event.objects.create(
            user=self.user,
            name='Test Event',
            description='Test Description',
            location='Test Location',
            event_start_date=timezone.now() + timezone.timedelta(days=1),
            event_end_date=timezone.now() + timezone.timedelta(days=2),
            registration_start_date=timezone.now(),
            registration_end_date=timezone.now() + timezone.timedelta(hours=1),
            max_participants=2,
            visibility=True
        )

    def test_create_registration(self):
        # Cria uma inscrição válida
        registration = Registration.objects.create(
            event=self.event,
            user=self.user,
            status='confirmed'
        )
        self.assertEqual(registration.event, self.event)
        self.assertEqual(registration.user, self.user)
        self.assertEqual(registration.status, 'confirmed')
        self.assertIsNotNone(registration.registration_date)

    def test_registration_default_status(self):
        # Verifica se o status padrão é 'pending'
        registration = Registration.objects.create(
            event=self.event,
            user=self.user
        )
        self.assertEqual(registration.status, 'pending')

    def test_registration_unique_together(self):
        # Tenta criar duas inscrições para o mesmo usuário e evento
        Registration.objects.create(event=self.event, user=self.user)
        with self.assertRaises(Exception):  # Django lança uma exceção ao violar unique_together
            Registration.objects.create(event=self.event, user=self.user)

    def test_registration_participant_limit(self):
        # Cria inscrições até atingir o limite de participantes
        user2 = User.objects.create_user(username='testuser2', password='12345')
        Registration.objects.create(event=self.event, user=self.user)
        Registration.objects.create(event=self.event, user=user2)

        # Tenta criar uma terceira inscrição, o que deve falhar
        user3 = User.objects.create_user(username='testuser3', password='12345')
        registration = Registration(event=self.event, user=user3)
        with self.assertRaises(ValidationError):
            registration.full_clean()  # Chama o método clean() para validar

    def test_registration_participant_limit_edge_case(self):
        # Verifica o limite exato de participantes
        user2 = User.objects.create_user(username='testuser2', password='12345')
        Registration.objects.create(event=self.event, user=self.user)
        Registration.objects.create(event=self.event, user=user2)

        # Verifica se o limite foi atingido
        self.assertEqual(self.event.registration_set.count(), 2)
        self.assertTrue(self.event.registration_set.count() == self.event.max_participants)


class RegisterViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.event = Event.objects.create(
            user=self.user,
            name='Test Event',
            description='Test Description',
            location='Test Location',
            event_start_date=timezone.now() + timezone.timedelta(days=1),
            event_end_date=timezone.now() + timezone.timedelta(days=2),
            registration_start_date=timezone.now(),
            registration_end_date=timezone.now() + timezone.timedelta(hours=1),
            max_participants=2,
            visibility=True
        )
        self.client.login(username='testuser', password='testpass')  # Autentica o usuário

    def test_successful_registration(self):
        response = self.client.post(reverse('register_in_event', args=[self.event.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('details_event', args=[self.event.id]))
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Inscrição realizada com sucesso!")
        
        self.assertTrue(Registration.objects.filter(user=self.user, event=self.event).exists())
        self.event.refresh_from_db()
        self.assertEqual(self.event.current_participants, 1)

    def test_registration_outside_period(self):
        self.event.registration_start_date = timezone.now() + timezone.timedelta(days=1)
        self.event.save()
        
        response = self.client.post(reverse('register_in_event', args=[self.event.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('details_event', args=[self.event.id]))
        
        self.assertFalse(Registration.objects.filter(user=self.user, event=self.event).exists())
        self.event.refresh_from_db()
        self.assertEqual(self.event.current_participants, 0)

    def test_event_full(self):
        self.event.current_participants = self.event.max_participants
        self.event.save()
        
        response = self.client.post(reverse('register_in_event', args=[self.event.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('details_event', args=[self.event.id]))
        
        self.assertFalse(Registration.objects.filter(user=self.user, event=self.event).exists())
        self.event.refresh_from_db()
        self.assertEqual(self.event.current_participants, self.event.max_participants)

    def test_user_already_registered(self):
        Registration.objects.create(user=self.user, event=self.event)
        self.event.current_participants = 1
        self.event.save()
        
        response = self.client.post(reverse('register_in_event', args=[self.event.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('details_event', args=[self.event.id]))
        
        self.assertEqual(Registration.objects.filter(user=self.user, event=self.event).count(), 1)
        self.event.refresh_from_db()
        self.assertEqual(self.event.current_participants, 1)

    def test_database_error(self):
        # Simulate a database error by forcing a rollback
        with self.assertRaises(DatabaseError):
            with transaction.atomic():
                # Forçando um erro de banco de dados
                Registration.objects.create(user=self.user, event=self.event)
                self.event.current_participants += 1
                self.event.save()
                raise DatabaseError("Simulated database error")
        
        self.assertFalse(Registration.objects.filter(user=self.user, event=self.event).exists())
        self.event.refresh_from_db()
        self.assertEqual(self.event.current_participants, 0)