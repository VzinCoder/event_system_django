
from django.urls import path
from .views import list_events_user,create_event,edit_event,delete_event,details_event,get_profile,list_events

urlpatterns = [
    path("",list_events,name="events"),
    path('myEvents/',list_events_user,name='my_events'),
    path('create/',create_event,name='create_event'),
    path('event/details/<int:id>/', details_event, name='details_event'),
    path('event/edit/<int:id>/', edit_event, name='edit_event'),
    path('event/delete/<int:id>/', delete_event, name='delete_event'),
    path('profile/',get_profile,name='profile'),
    
]
