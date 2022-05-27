from django.urls import path, re_path
from . import views

urlpatterns = [
    # /playlist/
    #re_path(r'^.*', views.index, name='playlist_index'),
    path('', views.index, name='playlist-index'),
    # ex: /playlist/spfy-playlists/?<user>
    path('spfy-playlists/', views.spotifyGetUserPlaylists, {}, name='spotify-spotifyGetUserPlaylists'),    
]