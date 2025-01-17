from django import forms
from .models import Event
from django.utils import timezone

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description','image','location', 'event_start_date','event_end_date','max_participants','registration_start_date','registration_end_date','visibility']

        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'image':"Imagem do Evento",
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
            'image': forms.FileInput(attrs={'class': 'form-control','required':False})
        }


    def clean_registration_start_date(self):
        reg_start_date = self.cleaned_data.get('registration_start_date')
        if reg_start_date and reg_start_date < timezone.now():
            raise forms.ValidationError("A data de início das inscrições não pode estar no passado.")
        return reg_start_date

    def clean_registration_end_date(self):
        reg_end_date = self.cleaned_data.get('registration_end_date')
        reg_start_date = self.cleaned_data.get('registration_start_date')
        if reg_end_date and reg_start_date and reg_end_date < reg_start_date:
            raise forms.ValidationError("A data de término das inscrições deve ser posterior à data de início das inscrições.")
        return reg_end_date

    def clean_event_start_date(self):
        event_start_date = self.cleaned_data.get('event_start_date')
        reg_end_date = self.cleaned_data.get('registration_end_date')
        if event_start_date and event_start_date < timezone.now():
            raise forms.ValidationError("A data de início do evento não pode estar no passado.")
        if event_start_date and reg_end_date and event_start_date < reg_end_date:
            raise forms.ValidationError("A data de início do evento deve ser posterior à data de término das inscrições.")
        return event_start_date

    def clean_event_end_date(self):
        event_end_date = self.cleaned_data.get('event_end_date')
        event_start_date = self.cleaned_data.get('event_start_date')
        if event_end_date and event_start_date and event_end_date < event_start_date:
            raise forms.ValidationError("A data de término do evento deve ser posterior à data de início do evento.")
        return event_end_date
