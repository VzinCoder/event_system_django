from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Event
from .forms import EventForm
from django.urls import reverse
from django.contrib.auth.models import User
from events.views import create_event,delete_event,details_event,list_events,edit_event,list_events_user
from django.contrib.messages import get_messages


class EventModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )
        self.event_start_date = timezone.now() + timezone.timedelta(days=1)
        self.event_end_date = self.event_start_date + timezone.timedelta(hours=2)
        self.registration_start_date = timezone.now()
        self.registration_end_date = self.registration_start_date + timezone.timedelta(days=1)

    def test_create_event(self):
        event = Event.objects.create(
            user=self.user,
            name="Evento de Teste",
            description="Descrição do evento de teste",
            location="Local do evento",
            event_start_date=self.event_start_date,
            event_end_date=self.event_end_date,
            registration_start_date=self.registration_start_date,
            registration_end_date=self.registration_end_date,
            current_participants=0,
            max_participants=50,
            visibility=True
        )

        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(event.name, "Evento de Teste")  
        self.assertEqual(event.description, "Descrição do evento de teste") 
        self.assertEqual(event.location, "Local do evento")  
        self.assertEqual(event.visibility, True)  
        self.assertEqual(event.event_start_date, self.event_start_date)  
        self.assertEqual(event.event_end_date, self.event_end_date) 
        self.assertEqual(event.registration_start_date, self.registration_start_date)
        self.assertEqual(event.registration_end_date, self.registration_end_date) 
        self.assertEqual(event.current_participants, 0)  
        self.assertEqual(event.max_participants, 50) 

class EventFormTest(TestCase):

    def setUp(self):
        self.current_time = timezone.now()

    def test_valid_form(self):
        form_data = {
            'name': 'Evento Teste',
            'description': 'Descrição do evento',
            'location': 'Local do evento',
            'event_start_date': self.current_time + timezone.timedelta(days=1),
            'event_end_date': self.current_time + timezone.timedelta(days=2),
            'registration_start_date': self.current_time + timezone.timedelta(hours=1),
            'registration_end_date': self.current_time + timezone.timedelta(hours=2),
            'max_participants': 100,
            'visibility': True,
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_registration_start_date(self):
        form_data = {
            'name': 'Evento Teste',
            'description': 'Descrição do evento',
            'location': 'Local do evento',
            'event_start_date': self.current_time + timezone.timedelta(days=1),
            'event_end_date': self.current_time + timezone.timedelta(days=2),
            'registration_start_date': self.current_time - timezone.timedelta(days=1),
            'registration_end_date': self.current_time + timezone.timedelta(hours=2),
            'max_participants': 100,
            'visibility': True,
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('registration_start_date', form.errors)

    def test_invalid_registration_end_date(self):
        form_data = {
            'name': 'Evento Teste',
            'description': 'Descrição do evento',
            'location': 'Local do evento',
            'event_start_date': self.current_time + timezone.timedelta(days=1),
            'event_end_date': self.current_time + timezone.timedelta(days=2),
            'registration_start_date': self.current_time + timezone.timedelta(hours=1),
            'registration_end_date': self.current_time - timezone.timedelta(hours=1),
            'max_participants': 100,
            'visibility': True,
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('registration_end_date', form.errors)

    def test_invalid_event_start_date(self):
        form_data = {
            'name': 'Evento Teste',
            'description': 'Descrição do evento',
            'location': 'Local do evento',
            'event_start_date': self.current_time - timezone.timedelta(days=1),
            'event_end_date': self.current_time + timezone.timedelta(days=2),
            'registration_start_date': self.current_time + timezone.timedelta(hours=1),
            'registration_end_date': self.current_time + timezone.timedelta(hours=2),
            'max_participants': 100,
            'visibility': True,
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('event_start_date', form.errors)

    def test_invalid_event_end_date(self):
        form_data = {
            'name': 'Evento Teste',
            'description': 'Descrição do evento',
            'location': 'Local do evento',
            'event_start_date': self.current_time + timezone.timedelta(days=1),
            'event_end_date': self.current_time - timezone.timedelta(days=1),
            'registration_start_date': self.current_time + timezone.timedelta(hours=1),
            'registration_end_date': self.current_time + timezone.timedelta(hours=2),
            'max_participants': 100,
            'visibility': True,
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('event_end_date', form.errors)

    def test_event_start_date_before_registration_end_date(self):
        form_data = {
            'name': 'Evento Teste',
            'description': 'Descrição do evento',
            'location': 'Local do evento',
            'event_start_date': self.current_time + timezone.timedelta(hours=1),
            'event_end_date': self.current_time + timezone.timedelta(days=2),
            'registration_start_date': self.current_time + timezone.timedelta(hours=2),
            'registration_end_date': self.current_time + timezone.timedelta(hours=3),
            'max_participants': 100,
            'visibility': True,
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('event_start_date', form.errors)

    def test_event_end_date_before_event_start_date(self):
        form_data = {
            'name': 'Evento Teste',
            'description': 'Descrição do evento',
            'location': 'Local do evento',
            'event_start_date': self.current_time + timezone.timedelta(days=2),
            'event_end_date': self.current_time + timezone.timedelta(days=1),
            'registration_start_date': self.current_time + timezone.timedelta(hours=1),
            'registration_end_date': self.current_time + timezone.timedelta(hours=2),
            'max_participants': 100,
            'visibility': True,
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('event_end_date', form.errors)


class EventViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.event = Event.objects.create(
            user=self.user,
            name='Test Event',
            description='Test Description',
            location='Test Location',
            event_start_date=timezone.now() + timezone.timedelta(days=1),
            event_end_date=timezone.now() + timezone.timedelta(days=2),
            registration_start_date=timezone.now(),
            registration_end_date=timezone.now() + timezone.timedelta(hours=1),
            max_participants=10,
            visibility=True
        )

    def test_create_event_get(self):
        response = self.client.get(reverse('create_event'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_create_event_post(self):
        data = {
            'name': 'New Event',
            'description': 'New Description',
            'location': 'New Location',
            'event_start_date': (timezone.now() + timezone.timedelta(days=1)),
            'event_end_date': (timezone.now() + timezone.timedelta(days=2)),
            'registration_start_date': timezone.now() + timezone.timedelta(hours=1),
            'registration_end_date': timezone.now() + timezone.timedelta(hours=2),
            'max_participants': 10,
            'visibility': True
        }
        response = self.client.post(reverse('create_event'), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento esperado
        self.assertEqual(Event.objects.count(), 2)

    def test_edit_event_get(self):
        response = self.client.get(reverse('edit_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_edit_event_post(self):
        data = {
            'name': 'Updated Event',
            'description': 'Updated Description',
            'location': 'Updated Location',
            'event_start_date': (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            'event_end_date': (timezone.now() + timezone.timedelta(days=2)).isoformat(),
            'registration_start_date': timezone.now() + timezone.timedelta(hours=1),
            'registration_end_date': timezone.now() + timezone.timedelta(hours=2),
            'max_participants': 20,
            'visibility': False
        }
        response = self.client.post(reverse('edit_event', args=[self.event.id]), data)
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, 'Updated Event')

    def test_details_event(self):
        response = self.client.get(reverse('details_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('event', response.context)

    def test_delete_event(self):
        response = self.client.post(reverse('delete_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 0)

    def test_list_events_user(self):
        response = self.client.get(reverse('my_events'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('events', response.context)

    def test_list_events(self):
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('events', response.context)