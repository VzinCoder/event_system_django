from django import forms
from .models import Event
from django.utils import timezone
from zoneinfo import ZoneInfo
class EventForm(forms.ModelForm):
    timezone = forms.CharField(widget=forms.HiddenInput(),required=True)
    class Meta:
        model = Event
        fields = ['name', 'description', 'image', 'location', 'event_start_date', 'event_end_date', 
                  'max_participants', 'registration_start_date', 'registration_end_date', 'visibility']

        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'image': "Imagem do Evento",
            'location': 'Localização',
            'event_start_date': 'Data de Início do Evento',
            'event_end_date': 'Data de Término do Evento',
            'registration_start_date': 'Data de Início das Inscrições',
            'registration_end_date': 'Data de Término das Inscrições',
            'max_participants': 'Máximo de Participantes',
            'visibility': 'Visibilidade do Evento',
        }

        widgets = {
            'event_start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'event_end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'registration_start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'registration_end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'visibility': forms.Select(
                attrs={'class': 'form-select'}, 
                choices=[(True, 'Público'), (False, 'Privado')]
            ),
            'image': forms.FileInput(attrs={'class': 'form-control', 'required': False})
        }

    def convert_data_to_utc(self, dt):
        if not dt:
            return None  # Retorna None se a data não for fornecida
        
        timezone_str = self.data.get('timezone')
        if not timezone_str:
            return dt  # Retorna a data original se o fuso horário não for fornecido
        
        try:
            tz_user = ZoneInfo(timezone_str)
            dt = dt.replace(tzinfo=tz_user)
            return dt.astimezone(ZoneInfo("UTC"))
        except Exception:
            self.add_error('timezone', "Fuso horário inválido.")  # Adiciona um erro no formulário
            return dt  # Retorna a data original para evitar falhas

    def clean_event_start_date(self):
        event_start_date = self.cleaned_data.get('event_start_date')
        return self.convert_data_to_utc(event_start_date)

    def clean_event_end_date(self):
        event_end_date = self.cleaned_data.get('event_end_date')
        return self.convert_data_to_utc(event_end_date)

    def clean_registration_start_date(self):
        registration_start_date = self.cleaned_data.get('registration_start_date')
        return self.convert_data_to_utc(registration_start_date)

    def clean_registration_end_date(self):
        registration_end_date = self.cleaned_data.get('registration_end_date')
        return self.convert_data_to_utc(registration_end_date)
    
    def clean(self):
        cleaned_data = super().clean()
        
        event_start_date = cleaned_data.get('event_start_date')
        event_end_date = cleaned_data.get('event_end_date')
        registration_start_date = cleaned_data.get('registration_start_date')
        registration_end_date = cleaned_data.get('registration_end_date')
        
        # Validação da data de início das inscrições
        if registration_start_date and registration_start_date < timezone.now():
            self.add_error('registration_start_date', "A data de início das inscrições não pode estar no passado.")

        # Validação da data de término das inscrições
        if registration_end_date and registration_start_date and registration_end_date < registration_start_date:
            self.add_error('registration_end_date', "A data de término das inscrições deve ser posterior à data de início das inscrições.")

        # Validação da data de início do evento
        if event_start_date and event_start_date < timezone.now():
            self.add_error('event_start_date', "A data de início do evento não pode estar no passado.")

        if event_start_date and registration_end_date and event_start_date < registration_end_date:
            self.add_error('event_start_date', "A data de início do evento deve ser posterior à data de término das inscrições.")

        # Validação da data de término do evento
        if event_end_date and event_start_date and event_end_date < event_start_date:
            self.add_error('event_end_date', "A data de término do evento deve ser posterior à data de início do evento.")

        return cleaned_data
