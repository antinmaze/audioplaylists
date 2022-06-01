from typing import List

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
class Item(object):
    
    #attributes
    name = ''
    description = ''
    external_urls = ''
    href = ''
    id = ''
    image_url = ''
    owner_name = ''
    tracks_url = ''
    tracks_total = ''

    #class default constructor
    def __init__(self,name,description, external_urls, href, id, image_url,
    owner_name, tracks_url, tracks_total):

      self.name = name
      self.description = description
      self.external_urls = external_urls
      self.href = href
      self.id = id
      self.image_url = image_url
      self.owner_name = owner_name
      self.tracks_url = tracks_url
      self.tracks_total = tracks_total


class Playlist(object):
    def __init__(self, items: List[Item]):
        self.items = items