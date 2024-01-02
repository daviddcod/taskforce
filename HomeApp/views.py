from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def beats(request):
    return render(request, 'HomeApp/beats.html' )

from django.shortcuts import render
from wdmmorpg.models import Task
from music.models import Playlist
from myblog.models import Blog

def welcome(request):
    # Fetch the first instances for the carousel
    task = Task.objects.first()
    playlist = Playlist.objects.first()
    blog = Blog.objects.first()

    # Fetch all instances for the sections
    tasks = Task.objects.all()
    playlists = Playlist.objects.all()
    blogs = Blog.objects.all()

    context = {
        'task': task,
        'playlist': playlist,
        'blog': blog,
        'tasks': tasks,
        'playlists': playlists,
        'blogs': blogs,
    }
    return render(request, 'HomeApp/welcome.html', context)

def home(request):
    cookies_accepted = request.session.get('cookie_consent', False)
    return render(request, 'wdm_home.html', {'cookies_accepted': cookies_accepted})

@csrf_exempt
def set_cookie(request):
    if request.method == 'POST':
        request.session['cookie_consent'] = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)