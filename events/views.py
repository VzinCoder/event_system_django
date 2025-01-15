from django.shortcuts import get_object_or_404, render,redirect
from .forms import EventForm
from .models import Event
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required
def create_event(request):
    templateData  =  {
        'title':'Criar Evento',
        'button_text':'Criar Evento'
    }

    if request.method == 'GET':
        templateData['form'] = EventForm()
        return render(request, 'event-form.html', templateData)
    
    form = EventForm(request.POST)
    if form.is_valid():
       event = form.save(commit=False)
       event.user = request.user  
       event.save()
       return redirect('my_events')
    
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
    
    form = EventForm(request.POST, instance=event)
    if form.is_valid():
       form.save()
       return redirect('my_events')
    
    templateData['form'] = form
    return render(request, 'event-form.html',templateData)


def details_event(request,id):
    event = get_object_or_404(Event, id=id)
    return render(request,'details.html',{'event':event})

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
    events = Event.objects.all()
    paginator = Paginator(events,6)
    page_number = request.GET.get('page')
    events_paginate = paginator.get_page(page_number)
    return render(request, 'events.html', {'events': events_paginate})


@login_required
def get_profile(request):
    return render(request,'profile.html')