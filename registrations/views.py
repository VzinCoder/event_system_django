from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Registration
from events.models import Event
from django.utils.timezone import now
from django.db import DatabaseError, transaction
from django.core.paginator import Paginator


@login_required
def register(request, id):
    if request.method != "POST":
        return redirect("details_event", id=id)
    
    event = get_object_or_404(Event, id=id)

    if not (event.registration_start_date <= now() <= event.registration_end_date):
        return redirect("details_event", id=id)

    try:
        with transaction.atomic():
            event = Event.objects.select_for_update().get(id=id)
            # event = Event.objects.filter(id = id).first()
            if event.current_participants >= event.max_participants:
                return redirect("details_event", id=id)

            if not Registration.objects.filter(user=request.user, event=event).exists():
                Registration.objects.create(user=request.user, event=event)
                event.current_participants += 1
                event.save(update_fields=["current_participants"])
                messages.success(request, "Inscrição realizada com sucesso!")
    except DatabaseError:
        messages.error(request, "Ocorreu um erro durante a inscrição. Tente novamente.")

    return redirect("details_event", id=id)



def my_registrations(request):
    if not request.user.is_authenticated:
        return render(request, 'my_registrations.html')
    registrations = Registration.objects.filter(user=request.user)

    # Configurar a paginação
    paginator = Paginator(registrations, 6)  # 6 inscrições por página
    page_number = request.GET.get('page')  # Obtém o número da página via GET
    page_obj = paginator.get_page(page_number)  # Obtém a página atual

    # Passar o objeto de paginação para o template
    return render(request, 'my_registrations.html', {'registrations': page_obj})