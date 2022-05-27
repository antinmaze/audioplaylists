from django.urls import path

from . import views

urlpatterns = [
    # ex: /oauth/
    path('', views.spotifyAuthorizationRequest, name='spotify-authorizationRequest'),
    # ex: /oauth/spfy-callback/
    path('spfy-callback/', views.spotifyRequestAccess, {}, name='spotify-spotifyRequestAccess'),
]