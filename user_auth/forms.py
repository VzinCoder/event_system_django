from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do usuario'}),
        label='Nome do usuario'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label='Senha'
    )


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Primeiro Nome",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputFirstName',
            'placeholder': 'Digite seu primeiro nome',
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Sobrenome",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputLastName',
            'placeholder': 'Digite seu sobrenome',
        })
    )
    email = forms.EmailField(
        required=True,
        label="Endereço de E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'inputEmail',
            'placeholder': 'nome@exemplo.com',
        })
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'inputPassword',
            'placeholder': 'Crie uma senha',
        })
    )
    password2 = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'inputPasswordConfirm',
            'placeholder': 'Confirme a senha',
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_first_name(self):
        username = self.cleaned_data.get('first_name')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso. Por favor, escolha outro.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['first_name'] 
        if commit:
            user.save()
        return user