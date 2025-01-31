from django.urls import path
from .views import register,my_registrations

urlpatterns = [
    path("<int:id>",register,name="register_in_event"),
     path('my-registrations/', my_registrations, name='my_registrations')
]
