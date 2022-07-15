from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from oauth import session
import json
#from jsonpath_ng import jsonpath, parser
#from collections import namedtuple
from typing import List
from urllib.parse import parse_qs, urlparse
from django.http import JsonResponse

from .spotify import Playlist, Track

def index(request):
    #params = kwargs.pop('params', {})
    #get the spotify user attribute efrom the path ELSE get the user ID from session used during the AUth 
    spotify_id = request.GET.get(settings.ATTRIB_SPOTIFY_ID, '')
    #get the desired offset and the limit will be set to settings.SPOTIFY_PLAYLISTS_LIMIT
    nextoffset = request.GET.get(settings.ATTRIB_SPOTIFY_PLAYLISTS_OFFSET, 0)
    #set contextext
    context = {}
    context['spotify_id']=  spotify_id
    context['playlist_nxtoffset']=  nextoffset
    return render(request, 'playlist/index.html', context)


#GET https://localhost:8000/playlist/spfy-playlists/?spotify_id=etanova&offset=50
#MANAGE user=etanova &offset=0&limit=50
##   """ Response example:
##    {"href": "https://api.spotify.com/v1/me/shows?offset=0&limit=20\n",
##    "items": [{}],
##    "limit": 20,
##    "next": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
##    "offset": 0,
##    "previous": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
##    "total": 4 }
##    """
def spotifyGetPlaylists(request):
    #get the spotify user attributee from the path ELSE get the user ID from session used during the AUth 
    #spotify_id = request.GET.get(settings.ATTRIB_SPOTIFY_ID, request.session['spotify_id'])
    spotify_id = request.GET.get(settings.ATTRIB_SPOTIFY_ID, '')
    #get the desired offset and the limit will be set to settings.ATTRIB_SPOTIFY_PLAYLISTS_OFFSET
    spotify_offset = request.GET.get(settings.ATTRIB_SPOTIFY_PLAYLISTS_OFFSET, 0)

    #SPOTIFY_PLAYLISTS_PATH = '/playlists?offset=0&limit=50'
    #build the URL  https://api.spotify.com/v1/users/user_id/playlists?offset=0&limit=50'
    resource_url = (settings.SPOTIFY_USER_PATH + str(spotify_id) + settings.SPOTIFY_PLAYLISTS_PATH +
    settings.SPOTIFY_OFFSET+'='+str(spotify_offset)+'&'+settings.SPOTIFY_LIMIT+'='+
    str(settings.SPOTIFY_PLAYLISTS_LIMIT))

    #execute the request API
    data_api = session.ressourceRequest(request, resource_url, settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_TOKEN_URL)
    data_json = json.loads(data_api.decode('utf-8'))
    #data_json = json.loads(data_api)
    #return HttpResponse(str(data_json))
    next_offset = 0
    prev_offset = 0
    ctx = getOffsetAndLimit(data_json["next"])
    if ctx:
        next_offset = 0 if  ctx['offset'][0]== None else ctx['offset'][0] 
    ctx = getOffsetAndLimit(data_json["previous"])
    if ctx:
        prev_offset = 0 if  ctx['offset'][0]== None else ctx['offset'][0]

    #Get playlist data
    # creating playslists       
    playlists = [] 
    # Iterating through the json list
    for item in data_json["items"]:
        playlists.append(Playlist(
            item['name'],
            item['description'],
            item['external_urls']['spotify'],
            item['href'],
            item['id'],
            item['images'][0]['url'],
            item['owner']['display_name'],
            item['tracks']['href'],
            item['tracks']['total']
        ))
    context = {}
    context.update({'playlists': playlists, 'spotify_id': spotify_id,
    'playlist_nxtoffset' : next_offset, 'playlist_prvoffset' : prev_offset})
    return render(request, 'playlist/index.html', context)


"""
  "next" : "https://api.spotify.com/v1/users/etanova/playlists?offset=50&limit=50", 
  "offset" : 0,
  "previous" : null, 
  """
def getOffsetAndLimit(url):
    return parse_qs(urlparse(url).query)

"""
  "next" : "https://api.spotify.com/v1/users/etanova/playlists?offset=50&limit=50", 
  "offset" : 0,
  "previous" : null, 
  """
""" ex: /playlist/spfy-tracks/?<playlist_id> """
def spotifyGetTracks(request):
    #get the spotify user attribute efrom the path ELSE get the user ID from session used during the AUth 
    #spotify_id = request.GET.get(settings.ATTRIB_SPOTIFY_ID, request.session['spotify_id'])

    #get the od of the playlist settings.ATTRIB_SPOTIFY_PLAYLIST_ID
    spotify_playlist_id = request.GET.get(settings.ATTRIB_SPOTIFY_PLAYLIST_ID, 0)

    #SPOTIFY_PLAYLISTS_PATH = '/playlists?offset=0&limit=50'
    #build the URL  
    # "https://api.spotify.com/v1/playlists/2JzV6Psnc0PIG1V2cFqgFC/tracks
    resource_url = settings.SPOTIFY_PLAYLISTS_URL + str(spotify_playlist_id) + settings.SPOTIFY_TRACKS

    #execute the request API
    data_api = session.ressourceRequest(request, resource_url, settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_TOKEN_URL)
    data_json = json.loads(data_api.decode('utf-8'))
    #data_json = json.loads(data_api)
    #return HttpResponse(str(data_json))
    next_offset = 0
    prev_offset = 0
    ctx = getOffsetAndLimit(data_json["next"])
    if ctx:
        next_offset = 0 if  ctx['offset'][0]== None else ctx['offset'][0] 
    ctx = getOffsetAndLimit(data_json["previous"])
    if ctx:
        prev_offset = 0 if  ctx['offset'][0]== None else ctx['offset'][0]

    #Get tracks data
    # creating tracks       
    tracks = [] 
    # Iterating through the json list
    for item in data_json["items"]:
        tracks.append(Track(
            item['track']['name'], #name
            item['track']['artists'][0]['name'], #artist_name
            item['track']['external_ids']['isrc'], #external_id
            item['track']['external_urls']['spotify'], #external_urls
            item['track']['href'], #href
            item['track']['id'], #id
            item['track']['album']['images'][0]['url'] #image_url
        ))
    #load track objects as json string with key/value
    tracks_json = [json.dumps(track.__dict__) for track in tracks]

    context = {'tracks': tracks_json,'track_nxtoffset' : next_offset, 'track_prvoffset' : prev_offset}
    return JsonResponse(context, safe=True)
