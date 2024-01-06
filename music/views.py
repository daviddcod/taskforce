from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import Album, Song, Playlist
from .forms import SongForm, AlbumForm, PlaylistForm
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from .models import Song
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Playlist
from .serializers import SongSerializer

class PlaylistSongs(APIView):
    def get(self, request, playlist_id):
        playlist = Playlist.objects.get(id=playlist_id)
        songs = playlist.songs.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)


def batch_upload(request):
    if request.method == 'POST':
        for f in request.FILES.getlist('files'):
            file_extension = f.name.split('.')[-1].lower()
            if file_extension == 'mp3':
                audio = MP3(f)
                duration = int(audio.info.length)
            elif file_extension == 'wav':
                audio = WAVE(f)
                duration = int(audio.info.length)
            else:
                continue  # Skip unsupported file formats

            song = Song()
            song.title = f.name
            song.duration = duration
            song.audio_file.save(f.name, f, save=True)
        return redirect('music:song_list')
    return render(request, 'music/batch_upload.html')

def album_list(request):
    albums = Album.objects.all()
    return render(request, 'music/album_list.html', {'albums': albums})

def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    return render(request, 'music/album_detail.html', {'album': album})

def upload_song(request, album_id):
    album = Album.objects.get(id=album_id)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.album = album
            song.save()
            return redirect('music:album_detail', album_id=album.id)
    else:
        form = SongForm()
    return render(request, 'music/upload_song.html', {'form': form, 'album': album})

def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('music:album_list')
    else:
        form = AlbumForm()
    return render(request, 'music/create_album.html', {'form': form})

def edit_album(request, album_id):
    album = Album.objects.get(id=album_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('music:album_detail', album_id=album.id)
    else:
        form = AlbumForm(instance=album)
    return render(request, 'music/edit_album.html', {'form': form, 'album': album})

def delete_album(request, album_id):
    album = Album.objects.get(id=album_id)
    if request.method == 'POST':
        album.delete()
        return redirect('music:album_list')
    return render(request, 'music/delete_album.html', {'album': album})


# Create Song
def song_create(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('music:song_list')
    else:
        form = SongForm()
    return render(request, 'music/song_form.html', {'form': form})

def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        print("Form received:", form.is_valid(), form.errors, request.FILES)  # Debugging line

    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            
            # Check the file extension to determine the file type
            file_extension = str(song.audio_file).split('.')[-1].lower()
            try:
                if file_extension == 'mp3':
                    audio = MP3(song.audio_file)
                    song.duration = int(audio.info.length)
                elif file_extension == 'wav':
                    audio = WAVE(song.audio_file)
                    song.duration = int(audio.info.length)
                else:
                    form.add_error(None, "Unsupported file format.")
                    return render(request, 'music/song_add.html', {'form': form})

                song.save()
                return redirect('music:add_song')  # Redirect to the song list

            except Exception as e:
                print(f"Error processing audio file: {e}")
                form.add_error(None, "Error processing audio file.")

    else:
        form = SongForm()

    return render(request, 'music/song_add.html', {'form': form})

# List Songs
def song_list(request):
    songs = Song.objects.all()
    return render(request, 'music/song_list.html', {'songs': songs})

def song_list_all(request):
    songs = Song.objects.all().values('id', 'title')
    return JsonResponse(list(songs), safe=False)

# Update Song
def song_update(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return redirect('music:song_list')
    else:
        form = SongForm(instance=song)
    return render(request, 'music/song_form.html', {'form': form})

# Delete Song
def song_delete(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        song.delete()
        return redirect('music:song_list')
    return render(request, 'music/song_confirm_delete.html', {'song': song})


def playlist_create(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            # Create a new playlist instance but don't save it to the database yet
            playlist = form.save(commit=False)
            
            # Save the playlist to the database
            playlist.save()
            
            # Get the list of selected song IDs from the form
            selected_song_ids = form.cleaned_data.get('songs')
            
            # Retrieve the selected song objects based on the IDs and set them for the playlist
            selected_songs = Song.objects.filter(id__in=selected_song_ids)
            playlist.songs.set(selected_songs)
            
            # Save the changes to the playlist
            playlist.save()
            
            # Redirect to the playlist list page (or wherever is appropriate)
            return redirect('music:playlist_list')
    else:
        form = PlaylistForm()
    
    return render(request, 'music/playlist_create.html', {'form': form})

# List Playlists
def playlist_list(request):
    playlists = Playlist.objects.all()
    return render(request, 'music/playlist_list.html', {'playlists': playlists})

# Playlist Detail
from django.http import JsonResponse

def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    if request.method == 'POST':
        form = PlaylistForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()
            new_song = form.cleaned_data['songs'].last()  # Get the last added song
            return JsonResponse({'new_song_url': new_song.audio_file.url})
    else:
        form = PlaylistForm(instance=playlist)
    return render(request, 'music/playlist_detail.html', {'playlist': playlist, 'form': form})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def delete_song_ajax(request):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        playlist_id = request.POST.get('playlist_id')
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        song = get_object_or_404(Song, pk=song_id)
        playlist.songs.remove(song)
        updated_song_urls = [song.audio_file.url for song in playlist.songs.all()]
        return JsonResponse({'deleted': True, 'updated_song_urls': updated_song_urls})
    return JsonResponse({'deleted': False})

# views.py

from django.http import JsonResponse
from .models import Song  # Update with your actual model

def get_songs(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)  # Retrieve the specific playlist
        songs = playlist.songs.all().values('title', 'audio_file','id')  # Use 'title' instead of 'name'
        songs_data = list(songs)  # Convert QuerySet to a list of dictionaries
        return JsonResponse(songs_data, safe=False)  # Return response
    except Playlist.DoesNotExist:
        return JsonResponse({'error': 'Playlist not found'}, status=404)  # Handle the case where the playlist does not exist
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Handle other possible exceptions

def get_song(request, song_id):
    try:
        songs = Song.objects.all()
        songs = songs.all().values('title', 'audio_file','id')  # Use 'title' instead of 'name'
        songs_data = list(songs)  # Convert QuerySet to a list of dictionaries
        return JsonResponse(songs_data, safe=False)  # Return response
    except Playlist.DoesNotExist:
        return JsonResponse({'error': 'Playlist not found'}, status=404)  # Handle the case where the playlist does not exist
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Handle other possible exceptions