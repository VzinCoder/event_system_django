from django.shortcuts import get_object_or_404, render,redirect
from .forms import EventForm
from .models import Event

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
       form.save()
       return redirect('list_events')
    
    
    templateData['form'] = form
    return render(request, 'event-form.html',templateData)


def edit_event(request,id):
    event = get_object_or_404(Event, id=id)

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
       return redirect('list_events')
    
    templateData['form'] = form
    return render(request, 'event-form.html',templateData)


def details_event(request,id):
    event = get_object_or_404(Event, id=id)
    return render(request,'details.html',{'event':event})

def delete_event(request,id):
    evento = get_object_or_404(Event, id=id)
    evento.delete()
    return redirect('list_events')

def list_events(request):
    events = Event.objects.all()
    return render(request,'events.html', {'events':events})