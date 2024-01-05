from django.shortcuts import render

# Create your views here.
# chat/views.py

from django.shortcuts import render

# chat/views.py

from django.shortcuts import render, redirect

def index(request):
    room_name = request.GET.get('room_name')
    if room_name:
        return redirect('chat:room', room_name=room_name)
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/chatroom.html', {
        'room_name': room_name
    })