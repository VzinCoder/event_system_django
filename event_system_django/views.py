from django.shortcuts import get_object_or_404, render,redirect


def home_page(request):
    if request.user.is_authenticated:
        return redirect('events')
    return render(request,'home.html')