from django.shortcuts import get_object_or_404, render,redirect
from .forms import EventForm
from .models import Event
from django.contrib import messages

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


def delete_event(request, id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=id)
        event.delete()
        messages.success(request, f'Evento com o nome  "{event.name}" excluído com sucesso!')
        return redirect('list_events')
    else:
        return redirect('list_events')

def list_events(request):
    events = Event.objects.all()
    return render(request,'events.html', {'events':events})