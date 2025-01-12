from django.shortcuts import render,redirect
from .forms import CustomAuthenticationForm,CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout

def custom_login(request):
       if request.method == 'GET':
        form = CustomAuthenticationForm()
        return render(request, 'login.html', {'form': form})
    
       form = CustomAuthenticationForm(request, data=request.POST)
       if form.is_valid():
              username = form.cleaned_data.get('username')
              password = form.cleaned_data.get('password')
              user = authenticate(request, username=username, password=password)
              if user is None:
                      return render(request, 'login.html', {'form': form})
              login(request, user)
              return redirect('list_events')  
       return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'register.html',{'form':form})

    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
       form.save()
       return redirect('login')
    return render(request, 'register.html', {'form': form})

@login_required
def custom_logout(request):
     logout(request)
     return redirect('login')