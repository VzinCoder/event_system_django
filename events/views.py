from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from .forms import EventForm
from .models import Event
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from registrations.models import Registration
from django.utils.timezone import now


@login_required
def create_event(request):
    templateData  =  {
        'title':'Criar Evento',
        'button_text':'Criar Evento'
    }

    if request.method == 'GET':
        templateData['form'] = EventForm()
        return render(request, 'event-form.html', templateData)
    
    form = EventForm(request.POST,request.FILES)
    if form.is_valid():
       event = form.save(commit=False)
       event.user = request.user  
       event.save()
       return redirect('details_event',id=event.id)
    
    templateData['form'] = form
    return render(request, 'event-form.html',templateData)


@login_required
def edit_event(request,id):
    event = get_object_or_404(Event, id=id,user=request.user)
    templateData = {
        'title': 'Editar Evento',
        'button_text': 'Salvar Alterações'
    }

    if request.method == 'GET':
        templateData['form'] = EventForm(instance=event)
        return render(request, 'event-form.html', templateData)
    
    form = EventForm(request.POST,request.FILES, instance=event)
    if form.is_valid():
       form.save()
       return redirect('details_event',id=event.id)
    
    templateData['form'] = form
    return render(request, 'event-form.html',templateData)



def details_event(request, id):
    event = get_object_or_404(Event, id=id)
    event_url = reverse('details_event', args=[event.id])
    event_url_absolute = request.build_absolute_uri(event_url)

    user_is_registered = False
    registrations_closed = False
    event_full = False

    if request.user.is_authenticated:
        user_is_registered = Registration.objects.filter(user=request.user, event=event).exists()

    registrations_closed = not (event.registration_start_date <= now() <= event.registration_end_date)
    event_full = event.current_participants >= event.max_participants

    if user_is_registered:
        messages.warning(request, "Você já está inscrito neste evento!")
    elif registrations_closed:
        messages.warning(request, "As inscrições para este evento não estão abertas no momento.")
    elif event_full:
        messages.warning(request, "O limite de participantes para este evento foi atingido.")

    disable_btn = registrations_closed or event_full or user_is_registered
    return render(
        request, 
        'details.html', 
        {
            'event': event, 
            'event_url_absolute': event_url_absolute,
            'disable_btn': disable_btn,
        }
    )

@login_required
def delete_event(request, id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=id,user=request.user)
        event.delete()
        messages.success(request, f'Evento com o nome  "{event.name}" excluído com sucesso!')
        return redirect('my_events')
    else:
        return redirect('my_events')

def list_events_user(request):
    if not request.user.is_authenticated:
       return render(request, 'user-events.html')
    events = Event.objects.filter(user=request.user)
    return render(request, 'user-events.html', {'events': events})

def list_events(request):
    search_query = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)
    events_query = Event.objects.filter(visibility=True)

    if search_query:
        events_query = events_query.filter(name__icontains=search_query)

    events_query = events_query.order_by('-event_start_date', '-current_participants')

    paginator = Paginator(events_query,6)
    events_paginate = paginator.get_page(page_number)

    return render(request, 'events.html', {
        'events': events_paginate,
        'search': search_query 
    })



@login_required
def get_profile(request):
    return render(request,'profile.html')