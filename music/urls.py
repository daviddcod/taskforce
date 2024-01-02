from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('create_album/', views.create_album, name='create_album'),
    path('album/edit/<int:album_id>/', views.edit_album, name='edit_album'),
    path('album/delete/<int:album_id>/', views.delete_album, name='delete_album'),
    path('songs/', views.song_list, name='song_list'),
    path('song/create/', views.song_create, name='song_add'),
    path('song/add/', views.add_song, name='add_song'),
    path('song/<int:pk>/edit/',views.song_update, name='song_edit'),
    path('song/<int:pk>/delete/', views.song_delete, name='song_delete'),
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlist/add/', views.playlist_create, name='playlist_create'),
    path('playlist/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('api/songs/<int:playlist_id>/', views.get_songs, name='get_songs'),
    path('api/song/<int:song_id>/', views.get_song, name='get_song'),


]
