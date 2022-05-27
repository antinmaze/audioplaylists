from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from oauth import session
import json
#from jsonpath_ng import jsonpath, parser
from collections import namedtuple
from typing import List
from .spotify import Item

def index(request):
    #params = kwargs.pop('params', {})
    #get the spotify user attribute efrom the path ELSE get the user ID from session used during the AUth 
    #spotify_id = request.GET.get(settings.ATTRIB_SPOTIFY_ID, request.session['spotify_id'])
    spotify_id = request.GET.get(settings.ATTRIB_SPOTIFY_ID, '')
    #get the desired offset and the limit will be set to settings.SPOTIFY_PLAYLISTS_LIMIT
    spotify_offset = request.GET.get(settings.ATTRIB_SPOTIFY_OFFSET, 0)

    context = {}
    context['spotify_id']=  spotify_id
    context['spotify_offset']=  spotify_offset

    #if 'NEWVARIABLE' in request.GET:
        #TODO
    return render(request, 'playlist/index.html', context)


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


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
def spotifyGetUserPlaylists(request):
    #get the spotify user attribute efrom the path ELSE get the user ID from session used during the AUth 
    spotify_id = request.GET.get(settings.ATTRIB_SPOTIFY_ID, request.session['spotify_id'])
    #get the desired offset and the limit will be set to settings.SPOTIFY_PLAYLISTS_LIMIT
    spotify_offset = request.GET.get(settings.ATTRIB_SPOTIFY_OFFSET, 0)

    #SPOTIFY_PLAYLISTS_PATH = '/playlists?offset=0&limit=50'
    #build the URL  https://api.spotify.com/v1/users/user_id/playlists?offset=0&limit=50'
    resource_url = (settings.SPOTIFY_USER_PATH + str(spotify_id) + settings.SPOTIFY_PLAYLISTS_PATH +
    settings.ATTRIB_SPOTIFY_OFFSET+'='+str(spotify_offset)+'&'+settings.ATTRIB_SPOTIFY_LIMIT +
    str(settings.SPOTIFY_PLAYLISTS_LIMIT))

    #execute the request API
    data_api = session.ressourceRequest(request, resource_url, settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_TOKEN_URL)
    #data_json = json.loads(data_api.decode('utf-8'))
    data_json = json.loads(data_api)
    """
    { "href" : "https://api.spotify.com/v1/users/etanova/playlists?offset=0&limit=50",
    "items" : [
        
        { "collaborative" : false, 
        "description" : "NEW CHUNES + OLD JAMMERZ FOLLOW ON SPOTIFY // MERCH",
        "external_urls" : { "spotify" : "https://open.spotify.com/playlist/2JzV6Psnc0PIG1V2cFqgFC" },
        "href" : "https://api.spotify.com/v1/playlists/2JzV6Psnc0PIG1V2cFqgFC",
        "id" : "2JzV6Psnc0PIG1V2cFqgFC",
        "images" : [ { "height" : null, "url" : "https://i.scdn.co/image/ab67706c0000bebb16b33c4393bd8b9ab764b67f", "width" : null } ],
        "name" : "HEALTH PRIMER",
        "owner" : 
            { "display_name" : "HEALTH", 
            "external_urls" : { "spotify" : "https://open.spotify.com/user/healthnoise" },
            "href" : "https://api.spotify.com/v1/users/healthnoise", "id" : "healthnoise", "type" : "user", "uri" : "spotify:user:healthnoise" 
            },
        "primary_color" : null, "public" : false, "snapshot_id" : "MTE0LGU5MmI0ZTY1ODZjZGQ4YjNiNDc5NGY3ZWUzNWYyNjMxYjkxZWI4NjE=",
        "tracks" : 
            { "href" : "https://api.spotify.com/v1/playlists/2JzV6Psnc0PIG1V2cFqgFC/tracks", "total" : 17 }, 
        "type" : "playlist",
        "uri" : "spotify:playlist:2JzV6Psnc0PIG1V2cFqgFC" 
        },
    """
    #return HttpResponse(str(data_json))

    #Get playlist data
    # creating playslists       
    playlists = [] 
    # Iterating through the json list
    for item in data_json["items"]:
        playlists.append(Item(
            item['name'],
            item['description'],
            item['external_urls']['spotify'],
            item['href'],
            item['id'],
            item['images'][0]['url'],
            item['owner']['display_name'],
            item['tracks']['total']
        ))
    context = {}
    new_offset = int(spotify_offset) + int(settings.SPOTIFY_PLAYLISTS_LIMIT)
    context.update({'playlists': playlists, 'spotify_id': spotify_id,
    'spotify_offset' : new_offset})
    return render(request, 'playlist/index.html', context)


    return HttpResponse(str(playlists[0].image_url))


    """
    TODO Manage workers to get playlist data
    """
    #return HttpResponse(type(data_json))

    spotify_id = data_json['id']
    #adding context before redirect
    base_url = reverse('playlist-index')
    query_string =  urlencode({'spotify_id': spotify_id}) 
    redirect_url = '{}?{}'.format(base_url, query_string)
    return redirect(redirect_url)

