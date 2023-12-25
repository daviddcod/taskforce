from django import forms
from django.apps import apps
from django.core.exceptions import ValidationError

class SongForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('music', 'Song')  # Replace 'music' with your app's name
        fields = ['album', 'title', 'duration', 'audio_file']
        widgets = {
            'audio_file': forms.FileInput(attrs={'class': 'hidden-input'}),
        }
        
class AlbumForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('music', 'Album')
        fields = ['title', 'artist', 'release_date', 'cover_image']

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('music', 'Playlist')
        fields = ['title', 'songs']

