# views.py

from django.shortcuts import render

def about_me(request):
    return render(request, 'taskforce/about_me.html')
