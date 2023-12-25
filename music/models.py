from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='album_covers/')

    def __str__(self):
        return f"{self.title} by {self.artist}"

class Song(models.Model):
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.IntegerField()
    audio_file = models.FileField(upload_to='songs/')

    def __str__(self):
        return self.title

class Playlist(models.Model):
    title = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
