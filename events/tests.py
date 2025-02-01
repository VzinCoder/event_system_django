from django.test import TestCase
from django.utils import timezone
from .models import Event
from .forms import EventForm
from django.urls import reverse
from django.contrib.auth.models import User
from registrations.models import Registration

class EventModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.event_start_date = timezone.now() + timezone.timedelta(days=2)
        self.event_end_date = self.event_start_date + timezone.timedelta(hours=2)
        self.registration_start_date = timezone.now() + timezone.timedelta(hours=1)
        self.registration_end_date = self.registration_start_date + timezone.timedelta(hours=1)

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
            # a data de registration_start_date está no passado e deve falhar
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
            # a data de registration_end_date é menor que registration_start_date e deve falhar
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
            # a data de inicio do evento esta no passado e deve falhar
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
            # a data de event_end_date é menor que a data de event_start_date e deve falhar
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
            # data de event_start_date esta anterior a data de registration_end_date e deve falhar
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
            # a data de event_end_date é anterior a data de event_start_date e deve falhar
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

        # evento valido
        self.event = Event.objects.create(
            user=self.user,
            name='Test Event',
            description='Test Description',
            location='Test Location',
            event_start_date=timezone.now() + timezone.timedelta(days=1),
            event_end_date=timezone.now() + timezone.timedelta(days=2),
            registration_start_date = timezone.now() + timezone.timedelta(hours=1),
            registration_end_date = timezone.now() + timezone.timedelta(hours=2),
            max_participants=10,
            visibility=True
        )

    def test_create_event_user_not_authenticated(self):
        self.client.logout()
        url = reverse('create_event')
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("login")}?next={url}')
        

    def test_create_event_get(self):
        response = self.client.get(reverse('create_event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,template_name="event-form.html")
        self.assertIn('form',response.context)

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
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 2)
    
    def test_create_event_post_invalid(self):
        data = {
            'name': 'New Event',
            'description': 'New Description',
            'location': 'New Location',
            # event_start_date deve ser posterior a data atual
            'event_start_date': timezone.now(),
            'event_end_date': (timezone.now() + timezone.timedelta(days=2)),
            'registration_start_date': timezone.now() + timezone.timedelta(hours=1),
            'registration_end_date': timezone.now() + timezone.timedelta(hours=2),
            'max_participants': 10,
            'visibility': True
        }
        response = self.client.post(reverse('create_event'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,template_name="event-form.html")
        self.assertIn('form',response.context)
        # deve ser 1 pois o setUp inicia um evento
        self.assertEqual(Event.objects.count(), 1)

    def test_edit_event_user_not_authenticated(self):
        self.client.logout()
        url = reverse('edit_event',args=[self.event.id])
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("login")}?next={url}')
        
    def test_edit_event_get(self):
        response = self.client.get(reverse('edit_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,template_name="event-form.html")
        self.assertIn('form', response.context)

    def test_edit_event_post(self):
        data = {
            'name': 'Updated Event',
            'description': 'Updated Description',
            'location': 'Updated Location',
            'event_start_date': timezone.now() + timezone.timedelta(days=1),
            'event_end_date': timezone.now() + timezone.timedelta(days=2),
            'registration_start_date': timezone.now() + timezone.timedelta(hours=1),
            'registration_end_date': timezone.now() + timezone.timedelta(hours=2),
            'max_participants': 20,
            'visibility': False
        }
        response = self.client.post(reverse('edit_event', args=[self.event.id]), data)
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, data.get('name'))
        self.assertEqual(self.event.description, data.get('description'))
        self.assertEqual(self.event.location, data.get('location'))
        self.assertEqual(self.event.event_start_date,data.get('event_start_date'))
        self.assertEqual(self.event.event_end_date,data.get('event_end_date'))
        self.assertEqual(self.event.registration_start_date,data.get('registration_start_date'))
        self.assertEqual(self.event.registration_end_date,data.get('registration_end_date'))
        self.assertEqual(self.event.max_participants,data.get('max_participants'))
        self.assertEqual(self.event.visibility,data.get('visibility'))
    
    def test_edit_event_post_invalid(self):
        data = {
            'name': 'Updated Event',
            'description': 'Updated Description',
            'location': 'Updated Location',
            # event_start_date deve ser posterior a data atual
            'event_start_date': timezone.now(),
            'event_end_date': timezone.now() + timezone.timedelta(days=2),
            'registration_start_date': timezone.now() + timezone.timedelta(hours=1),
            'registration_end_date': timezone.now() + timezone.timedelta(hours=2),
            'max_participants': 20,
            'visibility': False
        }
        response = self.client.post(reverse('edit_event', args=[self.event.id]), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,template_name="event-form.html")
        self.assertIn('form', response.context)
        self.event.refresh_from_db()
        self.assertNotEqual(self.event.name,data.get('name'))

    def test_details_event_registrations_open(self):
        self.event.registration_start_date = timezone.now() - timezone.timedelta(hours=1)
        self.event.save(update_fields=['registration_start_date'])
        response = self.client.get(reverse('details_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,template_name="details.html")
        self.assertIn('event', response.context)
        messages_response = list(response.context.get('messages'))
        self.assertEqual(0,len(messages_response))
    
    def test_details_event_user_is_registered(self):
        Registration.objects.create(event=self.event,user=self.user)
        response = self.client.get(reverse('details_event',args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,template_name="details.html")
        self.assertIn('event', response.context)
        self.assertContains(response,'Você já está inscrito neste evento!')
        
    def test_details_event_registrations_closed(self):
        response = self.client.get(reverse('details_event',args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,template_name="details.html")
        self.assertIn('event', response.context)
        self.assertContains(response,"As inscrições para este evento não estão abertas no momento.")
    
    def test_details_event_full(self):
        # atingindo o limite de participantes 
        self.event.current_participants = self.event.max_participants 
        # alterando a data de inscrição para não exibir a msg 'As inscrições para este evento não estão abertas no momento.' 
        self.event.registration_start_date = timezone.now() - timezone.timedelta(hours=1)
        self.event.save(update_fields=['current_participants','registration_start_date'])
        response = self.client.get(reverse('details_event',args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,template_name="details.html")
        self.assertIn('event', response.context)
        self.assertContains(response,"O limite de participantes para este evento foi atingido.")

    def test_delete_event_user_not_authenticated(self):
        self.client.logout()
        url = reverse('delete_event',args=[self.event.id])
        response = self.client.post(url)
        self.assertRedirects(response, f'{reverse("login")}?next={url}')

    def test_delete_event_get(self):
        response = self.client.get(reverse('delete_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 1)

    def test_delete_event_post(self):
        response = self.client.post(reverse('delete_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 0)
    
    def test_list_events_user_is_authenticated(self):
        response = self.client.get(reverse('my_events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,template_name='user-events.html')
        self.assertTemplateNotUsed(response=response,template_name='verify-login.html')
        self.assertIn('events', response.context)
        events_response  = response.context.get('events')
        self.assertEqual(1,len(events_response))
        self.assertEqual(events_response.first(), self.event)

    def test_list_events_user_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('my_events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,template_name='user-events.html')
        self.assertTemplateUsed(response=response,template_name='verify-login.html')
        self.assertContains(response,'Você deseja fazer login ou criar uma conta?')
        self.assertNotIn('events', response.context)
        

    # methods  to test_list_events
    def private_event_default(self):
        self.event.visibility = False
        self.event.save(update_fields=['visibility'])

    def create_events_to_test_list_events(self):
        self.private_event_default()
        return [Event.objects.create(
            user=self.user,
            name=f'Test Event {i}',
            description=f'Test {i} Description {i}',
            location=f'Test Location {i}',
            event_start_date=timezone.now() + timezone.timedelta(days=1),
            event_end_date=timezone.now() + timezone.timedelta(days=2),
            registration_start_date = timezone.now() + timezone.timedelta(hours=1),
            registration_end_date = timezone.now() + timezone.timedelta(hours=2),
            max_participants=10,
            visibility= i < 10 # nove publicos e 3 privados
        ) for i in range(1,13)]
    
    def test_list_events_without_filters(self):
        events = self.create_events_to_test_list_events()
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events.html')
        events_response = response.context['events']
        # 6 itens por página
        self.assertEqual(len(events_response), 6)
        # Verifica que eventos privados não estão na lista
        for event in events[9:]:  # Os 3 últimos são privados
            self.assertNotIn(event, events_response)

    def test_list_events_with_search_filter(self):
        self.create_events_to_test_list_events()
        response = self.client.get(reverse('events'), {'search': 'Test Event 5'})
        self.assertEqual(response.status_code, 200)
        events_response = response.context['events']
        # Apenas um evento deve corresponder ao filtro
        self.assertEqual(len(events_response), 1)
        self.assertEqual(events_response[0].name, 'Test Event 5')

    def test_list_events_pagination_page_2(self):
        self.create_events_to_test_list_events()
        # testa se a paginacao esta funcionando
        response = self.client.get(reverse('events'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        events_response = response.context['events']
        # são 9 publicos no total e 6 por pagina logo na pagina 2 deve ter 3 eventos
        self.assertEqual(len(events_response), 3)

    def test_list_events_invalid_page_number(self):
        self.create_events_to_test_list_events()
        response = self.client.get(reverse('events'), {'page': 999})
        self.assertEqual(response.status_code, 200)
        # deve retornar a ultima pagina
        events_response = response.context['events']
        # a ultima pagina que é a 2 deve retornar 3 eventos
        self.assertEqual(len(events_response), 3)
    
    def test_get_profile_user_not_authenticated(self):
        self.client.logout()
        url = reverse('profile')
        response = self.client.post(url)
        self.assertRedirects(response, f'{reverse("login")}?next={url}')

    def test_get_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'profile.html')
        self.assertContains(response,self.user.username)