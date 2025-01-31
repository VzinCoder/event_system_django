from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import CustomAuthenticationForm,CustomUserCreationForm

class CustomAuthenticationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_valid_form(self):
        form_data = {'username': 'testuser', 'password': '12345'}
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'username': 'testuser', 'password': 'wrongpassword'}
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_empty_form(self):
        form_data = {'username': '', 'password': ''}
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'complexpassword123',
            'password2': 'differentpassword'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_existing_email(self):
        User.objects.create_user(username='existinguser', email='john.doe@example.com', password='12345')
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_existing_username(self):
        User.objects.create_user(username='John', email='john.doe@example.com', password='12345')
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe2@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_save_method(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'John')
        self.assertEqual(user.email, 'john.doe@example.com')

class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_get_request(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomAuthenticationForm)

    def test_post_request_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento para 'events'
        self.assertRedirects(response, reverse('events'))

    def test_post_request_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Permanece na página de login
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_post_request_empty_fields(self):
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

class RegisterViewTest(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_post_request_valid_data(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento para 'login'
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(email='john.doe@example.com').exists())

    def test_post_request_invalid_data(self):
        form_data = {
            'first_name': '',
            'last_name': '',
            'email': 'invalidemail',
            'password1': '123',
            'password2': '456'
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_post_request_existing_email(self):
        User.objects.create_user(username='existinguser', email='john.doe@example.com', password='12345')
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

class CustomLogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_logout_authenticated_user(self):
        self.client.login(username='testuser', password='12345')  # Autentica o usuário
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirecionamento para 'login'
        self.assertRedirects(response, reverse('login'))

    def test_logout_unauthenticated_user(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirecionamento para 'login'
        self.assertTrue(response.url.startswith(reverse('login')))  # Verifica se a URL começa com 