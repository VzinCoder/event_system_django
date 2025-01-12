from django.urls import path,include
from .views import custom_login,register,custom_logout

urlpatterns = [
    path('login/',custom_login,name='login'),
    path('register/',register,name='register'),
    path('logout/',custom_logout,name='logout')
]