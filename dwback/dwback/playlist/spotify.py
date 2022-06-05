from typing import List

class Track(object):
  name = '' #title
  artist_name = '' #TODO implement multi artists
  external_id = '' #isrc #TODO implement multi external_id
  external_urls = ''  
  href = ''
  id = ''
  image_url = '' #get the first image from the list

  #class default constructor
  def __init__(self,name, artist_name, external_id, 
  external_urls, href, id, image_url):
    self.name = name 
    self.artist_name = artist_name
    self.external_id = external_id
    self.external_urls = external_urls  
    self.href = href
    self.id = id 
    self.image_url = image_url


class Playlist(object):
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


#class Playlist(object):
#    def __init__(self, items: List[Item]):
#        self.items = items