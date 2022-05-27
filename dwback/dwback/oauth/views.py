from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
#from oauth.session import Session
from . import session
import json
#from django.http import QueryDict
from django.template import loader
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from django.conf import settings

# Implementing authorization code Request  # ex: /oauth/
def spotifyAuthorizationRequest(request):    
    authorization_url = session.authorizationRequest(request, settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_SCOPE, 
    settings.SPOTIFY_REDIRECT_URI, settings.SPOTIFY_AUTHORIZATION_BASE_URL)
    return redirect(authorization_url)


# Implementing Spotify token Request  # ex: /oauth/spfy-callback/
#@register.simple_tag(takes_context=True)
def spotifyRequestAccess(request):
    token = session.accessRequest(request, settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET, settings.SPOTIFY_SCOPE, 
    settings.SPOTIFY_REDIRECT_URI, settings.SPOTIFY_TOKEN_URL)
    """ TODO if token is None skip all the part an display error message HTTP 503 « Service is unavailable » 
    or a message error in spotify_id """
    
    #return HttpResponse(request.session['token'])
    if token != None :
        resource_url='https://api.spotify.com/v1/me'
        data_api = session.ressourceRequest(request, resource_url, settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_TOKEN_URL)
        #return HttpResponse(data_api)
        """
        example of spotify data_api
        { "display_name" : "Eltonio", "email" : "antoinemaze@free.fr", "external_urls" : 
        { "spotify" : "https://open.spotify.com/user/etanova" }, 
        "followers" : { "href" : null, "total" : 8 }, 
        "href" : "https://api.spotify.com/v1/users/etanova", 
        "id" : "etanova", "images" : [ ], "type" : "user", 
        "uri" : "spotify:user:etanova" }
        """
        data_json = json.loads(data_api.decode('utf-8'))
        spotify_id = data_json['id']
    #adding context before redirecting the the Playlist page
    base_url = reverse('playlist-index')
    query_string =  urlencode({settings.ATTRIB_SPOTIFY_ID: spotify_id}) 
    redirect_url = '{}?{}'.format(base_url, query_string)
    print (redirect_url)
    return redirect(redirect_url)
 