from django.test import Client, TestCase,TransactionTestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from events.models import Event
from .models import Registration
from django.contrib.messages import get_messages
import threading
from concurrent.futures import ThreadPoolExecutor,wait
from django.db import connections

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

class RegisterViewTest(TransactionTestCase):
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

    def test_registration_without_login(self):
        self.client.logout()  # Garante que o usuário está deslogado

        response = self.client.post(reverse('register_in_event', args=[self.event.id]))

        login_url = reverse('login')  # Ajuste conforme o nome da sua rota de login
        expected_redirect_url = f"{login_url}?next={reverse('register_in_event', args=[self.event.id])}"

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_redirect_url)
        self.assertFalse(Registration.objects.filter(user=self.user, event=self.event).exists())

    def test_get_request(self):
        response = self.client.get(reverse('register_in_event',args=[self.event.id]))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('details_event',args=[self.event.id]))

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
    
    def test_concurrent_registrations(self):
        self.event.max_participants = 2
        self.event.save()
        num_threads = 10  # Mais threads do que vagas para simular corrida
        barrier = threading.Barrier(num_threads)  # Sincroniza todas as threads antes do request
        
        def try_register(i):
            try:
                username = f'user_{i}'
                password = f'password_user{i}'
                client = Client()
                User.objects.create_user(username=username, password=password)
                client.login(username=username, password=password)
                barrier.wait()  # espera as outras threads
                client.post(reverse('register_in_event', args=[self.event.id]))
            finally:
                connections.close_all()

        #sobe as threads
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(lambda:try_register(i)) for i in range(num_threads)]
        
        # espera as threads terminarem
        wait(futures)
            
        self.event.refresh_from_db()
        registrations = Registration.objects.filter(event=self.event).count()

        self.assertEqual(registrations, self.event.max_participants) 
        self.assertEqual(self.event.current_participants, self.event.max_participants)
    
class MyRegistrationsViewTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        otherUser = User.objects.create_user(username='otheruser', password='otherpass')
        def create_event(i,user):
            return Event.objects.create(
            user=user,
            name=f'Name {i}',
            description=f'Description {i}',
            location=f'Location {i}',
            event_start_date=timezone.now() + timezone.timedelta(days=1),
            event_end_date=timezone.now() + timezone.timedelta(days=2),
            registration_start_date = timezone.now(),
            registration_end_date = timezone.now() + timezone.timedelta(hours=2),
            max_participants=10,
            visibility=True
            )
        self.events = [create_event(i,otherUser) for i in range(9)]
        
    def test_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('my_registrations'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'my_registrations.html')
        self.assertTemplateUsed(response,'verify-login.html')
    
    def test_logged_in(self):
        response = self.client.get(reverse('my_registrations'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'my_registrations.html')
        self.assertTemplateNotUsed(response,'verify-login.html')
        
    def test_empty_page(self):
        response = self.client.get(reverse('my_registrations'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'my_registrations.html')
        self.assertContains(response,'Nenhuma inscrição encontrada.')
    def popule_registration(self):
        # cria 9 Registration
        return [Registration.objects.create(event=event,user=self.user) for event in self.events]
                
    def test_pagination_default_page(self):
        self.popule_registration()
        response = self.client.get(reverse('my_registrations'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'my_registrations.html')
        self.assertIn('registrations',response.context)
        
        #retirando o paginator da response
        page_obj = response.context.get('registrations')
        paginator = page_obj.paginator
        # a paginacao deve ter duas paginas pois tem 9 registros e sao 6 por pagina
        self.assertEqual(2, paginator.num_pages)
        # a pagina 1 deve ter 6
        qty_events_page_one = len(page_obj.object_list)
        self.assertEqual(6,qty_events_page_one)
        # a pagina 2 deve ter 3
        qty_events_page_second = len(paginator.get_page(2))
        self.assertEqual(3,qty_events_page_second)
        # o total deve ser 9
        self.assertEqual(len(self.events),paginator.count)
    
    def test_pagination_page_2(self):
        self.popule_registration()
        response = self.client.get(reverse('my_registrations'),{'page':2})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'my_registrations.html')
        self.assertIn('registrations',response.context)
        #retirando o paginator da response
        page_obj = response.context.get('registrations')
        paginator = page_obj.paginator
        # a pagina 2 deve ter 3
        self.assertEqual(3,len(page_obj))
        # o total deve ser 9
        self.assertEqual(len(self.events),paginator.count)
    
    def test_pagination_order(self):
        registrations = self.popule_registration()
        response = self.client.get(reverse('my_registrations'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_registrations.html')
        self.assertIn('registrations', response.context)

        page_obj = response.context['registrations']
        if page_obj:
            first_item = page_obj[0]  # Primeiro item na página
            last_created = max(registrations, key=lambda r: r.registration_date)  # Último registro criado
            self.assertEqual(first_item.id, last_created.id) 