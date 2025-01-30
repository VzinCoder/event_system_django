from django.shortcuts import get_object_or_404, render,redirect


def home_page(request):
    return render(request,'home.html')