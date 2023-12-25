from django.shortcuts import render

# Create your views here.

def beats(request):
    return render(request, 'HomeApp/beats.html' )

def welcome(request):
    return render(request, 'HomeApp/welcome.html' )

